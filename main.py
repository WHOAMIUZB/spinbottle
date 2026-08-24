import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import sys

from database import (
    init_db, add_bot_token, get_all_bot_tokens, remove_bot_token,
    add_api_key, get_all_apis, update_api_price, remove_api,
    add_user, get_user_stats, ban_user, unban_user,
    create_promo_code, apply_promo_code, get_statistics, get_detailed_stats,
    log_broadcast
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MASTER_BOT_TOKEN = "8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg"
ADMIN_ID = 7861165622

# FSM States
class AdminStates(StatesGroup):
    adding_bot = State()
    adding_api = State()
    entering_api_name = State()
    entering_api_key = State()
    entering_api_price = State()
    entering_api_category = State()
    updating_api_price = State()
    removing_api = State()
    sending_broadcast = State()
    broadcast_type = State()
    broadcast_content = State()
    broadcast_select_bots = State()
    creating_promo = State()
    promo_code = State()
    promo_discount = State()
    promo_uses = State()
    banning_user = State()
    scheduling_message = State()
    schedule_time = State()
    schedule_content = State()

# Initialize bot and dispatcher
bot = Bot(token=MASTER_BOT_TOKEN)
dp = Dispatcher()

# Keyboards
def admin_main_keyboard():
    """Main admin panel keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Bot Qo'shish", callback_data="add_bot"),
         InlineKeyboardButton(text="🗑 Bot O'chirish", callback_data="remove_bot")],
        [InlineKeyboardButton(text="🔑 API Qo'shish", callback_data="add_api"),
         InlineKeyboardButton(text="📊 API Ro'yxat", callback_data="list_apis")],
        [InlineKeyboardButton(text="📢 Broadcast Yuborish", callback_data="send_broadcast"),
         InlineKeyboardButton(text="⏱ Xabar Jadvali", callback_data="schedule_message")],
        [InlineKeyboardButton(text="🎟 Promo Yaratish", callback_data="create_promo"),
         InlineKeyboardButton(text="👤 User Ban", callback_data="ban_user")],
        [InlineKeyboardButton(text="📈 Statistika", callback_data="show_stats"),
         InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
    ])

def bot_list_keyboard(bots: list):
    """Create keyboard with bot list"""
    keyboard = []
    for bot_info in bots:
        btn_text = f"🤖 {bot_info['bot_name']} ({bot_info['user_count']} users)"
        keyboard.append([InlineKeyboardButton(text=btn_text, callback_data=f"bot_{bot_info['token']}")])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Command Handlers
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    """Start command handler"""
    await add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    
    if message.from_user.id == ADMIN_ID:
        text = """
🔐 <b>SMM Master Bot - Admin Panel</b>

Xush kelibsiz! Bu bot barcha SMM botlaringizni boshqarish uchun yaratilgan.

Imkoniyatlar:
✅ Ko'plab bot tokenlarini bir joyda boshqarish
✅ API kalitlarini qo'shish/o'chirish
✅ Barcha botlarning foydalanuvchilariga broadcast xabar yuborish
✅ Promo kodlar yaratish
✅ Tola statistika ko'rish
✅ User management

/admin - Admin panelga kirish
        """
        await message.answer(text, parse_mode="HTML")
    else:
        text = """
🤖 <b>SMM Master Bot</b>

Salom! Bu bot orqali siz:
✅ Xizmatlarni sotib olishingiz mumkin
✅ Promo kodlarni qo'llashingiz mumkin
✅ Statistika ko'rishingiz mumkin

/help - To'liq ma'lumot
        """
        await message.answer(text, parse_mode="HTML")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Admin panel command"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    
    text = "<b>👑 Admin Panel</b>\n\nQanday qilishni xohlaysiz?"
    await message.answer(text, parse_mode="HTML", reply_markup=admin_main_keyboard())

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    """Help command"""
    text = """
<b>📖 Yordam Menyu</b>

<b>Foydalanuvchi Buyruqlari:</b>
/start - Botni boshlash
/help - Bu menyu
/balance - Hisobingizni ko'rish
/stats - Sizning statistika
/promo - Promo kodini qo'llash

<b>Admin Buyruqlari:</b>
/admin - Admin panelga kirish
/broadcast - Xabar yuborish
/bots - Barcha botlar
/apis - Barcha APIlar

Admin uchun: @admin_username
    """
    await message.answer(text, parse_mode="HTML")

# Admin Callback Handlers
@dp.callback_query(F.data == "add_bot")
async def add_bot_handler(callback: types.CallbackQuery, state: FSMContext):
    """Add bot handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🤖 Bot tokenini kiriting:\n\nMasalan: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg"
    )
    await state.set_state(AdminStates.adding_bot)

@dp.message(StateFilter(AdminStates.adding_bot))
async def process_bot_token(message: types.Message, state: FSMContext):
    """Process bot token input"""
    token = message.text.strip()
    
    if ":" not in token:
        await message.answer("❌ Noto'g'ri format! Token shaklini tekshiring.")
        return
    
    # Save token temporarily
    await state.update_data(bot_token=token)
    await message.answer("Bot nomi nima? (masalan: 'SMM Bot 1')")
    await state.set_state(AdminStates.adding_bot)

@dp.message(StateFilter(AdminStates.adding_bot))
async def process_bot_name(message: types.Message, state: FSMContext):
    """Process bot name input"""
    data = await state.get_data()
    token = data.get("bot_token")
    bot_name = message.text.strip()
    
    if await add_bot_token(token, bot_name):
        await message.answer(f"✅ Bot muvaffaqiyatli qo'shildi!\n\n🤖 {bot_name}")
    else:
        await message.answer("❌ Bot qo'shilmadi. Token allaqachon mavjud bo'lsa kerak.")
    
    await state.clear()

@dp.callback_query(F.data == "remove_bot")
async def remove_bot_handler(callback: types.CallbackQuery):
    """Remove bot handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    bots = await get_all_bot_tokens()
    if not bots:
        await callback.message.edit_text("❌ Bot topilmadi")
        return
    
    keyboard = bot_list_keyboard(bots)
    await callback.message.edit_text("O'chiriladigan botni tanlang:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("bot_"))
async def select_bot_handler(callback: types.CallbackQuery):
    """Select bot handler"""
    token = callback.data.replace("bot_", "")
    
    if await remove_bot_token(token):
        await callback.message.edit_text("✅ Bot muvaffaqiyatli o'chirildi!")
    else:
        await callback.message.edit_text("❌ Xato yuz berdi")

# API Management
@dp.callback_query(F.data == "add_api")
async def add_api_handler(callback: types.CallbackQuery, state: FSMContext):
    """Add API handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text("API nomi kiriting (masalan: 'OpenAI GPT')")
    await state.set_state(AdminStates.entering_api_name)

@dp.message(StateFilter(AdminStates.entering_api_name))
async def process_api_name(message: types.Message, state: FSMContext):
    """Process API name"""
    await state.update_data(api_name=message.text.strip())
    await message.answer("API kalitini kiriting:")
    await state.set_state(AdminStates.entering_api_key)

@dp.message(StateFilter(AdminStates.entering_api_key))
async def process_api_key(message: types.Message, state: FSMContext):
    """Process API key"""
    await state.update_data(api_key=message.text.strip())
    await message.answer("Narxi kiriting (masalan: 0.5):")
    await state.set_state(AdminStates.entering_api_price)

@dp.message(StateFilter(AdminStates.entering_api_price))
async def process_api_price(message: types.Message, state: FSMContext):
    """Process API price"""
    try:
        price = float(message.text.strip())
        await state.update_data(api_price=price)
        await message.answer("Kategoriya kiriting (masalan: 'Text Generation'):")
        await state.set_state(AdminStates.entering_api_category)
    except ValueError:
        await message.answer("❌ Raqam kiriting!")

@dp.message(StateFilter(AdminStates.entering_api_category))
async def process_api_category(message: types.Message, state: FSMContext):
    """Process API category"""
    data = await state.get_data()
    
    if await add_api_key(data['api_name'], data['api_key'], data['api_price'], message.text.strip()):
        await message.answer(
            f"✅ API qo'shildi!\n\n"
            f"📝 Nomi: {data['api_name']}\n"
            f"💰 Narxi: {data['api_price']}\n"
            f"📂 Kategoriya: {message.text.strip()}"
        )
    else:
        await message.answer("❌ API qo'shilmadi!")
    
    await state.clear()

@dp.callback_query(F.data == "list_apis")
async def list_apis_handler(callback: types.CallbackQuery):
    """List all APIs"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    apis = await get_all_apis()
    
    if not apis:
        await callback.message.edit_text("❌ API topilmadi")
        return
    
    text = "🔑 <b>Barcha APIlar:</b>\n\n"
    for api in apis:
        text += (
            f"<b>{api['api_name']}</b>\n"
            f"💰 Narxi: {api['price']} so'm\n"
            f"📊 Ishlatilgan: {api['used_requests']}/{api['limit_requests']}\n"
            f"📂 Kategoriya: {api['category']}\n"
            f"─────────────────────\n"
        )
    
    await callback.message.edit_text(text, parse_mode="HTML")

# Broadcast
@dp.callback_query(F.data == "send_broadcast")
async def send_broadcast_handler(callback: types.CallbackQuery, state: FSMContext):
    """Send broadcast handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Matn", callback_data="bc_text"),
         InlineKeyboardButton(text="🖼 Rasm", callback_data="bc_image")],
        [InlineKeyboardButton(text="🎥 Video", callback_data="bc_video"),
         InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")]
    ])
    
    await callback.message.edit_text("Broadcast turini tanlang:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("bc_"))
async def broadcast_type_handler(callback: types.CallbackQuery, state: FSMContext):
    """Broadcast type handler"""
    bc_type = callback.data.replace("bc_", "")
    await state.update_data(broadcast_type=bc_type)
    
    await callback.message.edit_text(
        f"{'📝 Matn' if bc_type == 'text' else '🖼 Rasm' if bc_type == 'image' else '🎥 Video'} kiriting:"
    )
    await state.set_state(AdminStates.broadcast_content)

@dp.message(StateFilter(AdminStates.broadcast_content))
async def process_broadcast_content(message: types.Message, state: FSMContext):
    """Process broadcast content"""
    data = await state.get_data()
    bc_type = data.get('broadcast_type')
    
    if bc_type == 'text':
        content = message.text
    elif bc_type == 'image':
        content = message.photo[-1].file_id if message.photo else None
    elif bc_type == 'video':
        content = message.video.file_id if message.video else None
    
    if not content:
        await message.answer("❌ Fayl topilmadi!")
        return
    
    bots = await get_all_bot_tokens()
    if not bots:
        await message.answer("❌ Bot topilmadi")
        return
    
    text = "Qaysi botlarga yuborasiz?\n\n"
    for i, bot in enumerate(bots):
        text += f"✅ {i+1}. {bot['bot_name']}\n"
    text += f"\nBarcha botlarga yuboriladi ({len(bots)} ta)"
    
    await message.answer(text)
    await message.answer("Yuborishni tasdiqlang? /yes yoki /no")
    await state.update_data(broadcast_content=content)
    await state.set_state(AdminStates.broadcast_select_bots)

# Statistics
@dp.callback_query(F.data == "show_stats")
async def show_stats_handler(callback: types.CallbackQuery):
    """Show statistics"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    stats = await get_statistics()
    detailed = await get_detailed_stats()
    
    text = (
        f"<b>📊 Asosiy Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {stats['total_users']}\n"
        f"📨 Jami xabarlar: {stats['total_messages']}\n"
        f"🤖 Faol botlar: {stats['active_bots']}\n"
        f"🔑 API ishlatilishi: {stats['api_usage']}\n\n"
        f"<b>Bot bo'yicha:</b>\n"
    )
    
    for bot_stat in detailed:
        text += (
            f"\n<b>{bot_stat['bot_name']}</b>\n"
            f"👥 {bot_stat['user_count']} users\n"
            f"💬 {bot_stat['message_count']} messages\n"
        )
    
    await callback.message.edit_text(text, parse_mode="HTML")

# Promo codes
@dp.callback_query(F.data == "create_promo")
async def create_promo_handler(callback: types.CallbackQuery, state: FSMContext):
    """Create promo handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text("Promo kodni kiriting (masalan: PROMO2024):")
    await state.set_state(AdminStates.promo_code)

@dp.message(StateFilter(AdminStates.promo_code))
async def process_promo_code(message: types.Message, state: FSMContext):
    """Process promo code"""
    await state.update_data(promo_code=message.text.strip().upper())
    await message.answer("Chegirma foizini kiriting (masalan: 20):")
    await state.set_state(AdminStates.promo_discount)

@dp.message(StateFilter(AdminStates.promo_discount))
async def process_promo_discount(message: types.Message, state: FSMContext):
    """Process promo discount"""
    try:
        await state.update_data(promo_discount=float(message.text.strip()))
        await message.answer("Maksimal foydalanish sonini kiriting:")
        await state.set_state(AdminStates.promo_uses)
    except ValueError:
        await message.answer("❌ Raqam kiriting!")

@dp.message(StateFilter(AdminStates.promo_uses))
async def process_promo_uses(message: types.Message, state: FSMContext):
    """Process promo max uses"""
    try:
        data = await state.get_data()
        max_uses = int(message.text.strip())
        
        if await create_promo_code(
            data['promo_code'],
            data['promo_discount'],
            max_uses,
            "2099-12-31"
        ):
            await message.answer(
                f"✅ Promo kod yaratildi!\n\n"
                f"🎟 Kod: {data['promo_code']}\n"
                f"🎁 Chegirma: {data['promo_discount']}%\n"
                f"📊 Max foydalanish: {max_uses}"
            )
        else:
            await message.answer("❌ Promo kod yaratilmadi!")
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Butun raqam kiriting!")

# User management
@dp.callback_query(F.data == "ban_user")
async def ban_user_handler(callback: types.CallbackQuery, state: FSMContext):
    """Ban user handler"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text("User ID sini kiriting:")
    await state.set_state(AdminStates.banning_user)

@dp.message(StateFilter(AdminStates.banning_user))
async def process_ban_user(message: types.Message, state: FSMContext):
    """Process ban user"""
    try:
        user_id = int(message.text.strip())
        if await ban_user(user_id):
            await message.answer(f"✅ User {user_id} bloklandi!")
        else:
            await message.answer("❌ Foydalanuvchi topilmadi!")
        await state.clear()
    except ValueError:
        await message.answer("❌ Butun raqam kiriting!")

# Back buttons
@dp.callback_query(F.data == "back_admin")
async def back_to_admin(callback: types.CallbackQuery):
    """Back to admin panel"""
    text = "<b>👑 Admin Panel</b>\n\nQanday qilishni xohlaysiz?"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_main_keyboard())

@dp.callback_query(F.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    """Back to main"""
    await callback.message.edit_text("🔙 Bosh menyu", reply_markup=admin_main_keyboard())

# Main function
async def main():
    """Start the bot"""
    await init_db()
    logger.info("Bot ishga tushdi!")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
