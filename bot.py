"""
Spin the Bottle - Telegram bot (aiogram 3.x)
Botning vazifasi: foydalanuvchiga Mini App (WebApp) tugmasini ko'rsatish.
O'yinning barcha logikasi web (FastAPI) tomonda ishlaydi.

Ishga tushirish: python bot.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo,
)

from config import BOT_TOKEN, ADMIN_ID, WEBAPP_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍾 O'ynash", web_app=WebAppInfo(url=WEBAPP_URL))],
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍾 O'ynash", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="⚙️ Admin panel", web_app=WebAppInfo(url=f"{WEBAPP_URL}/admin"))],
    ])


@dp.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id == ADMIN_ID:
        kb = admin_keyboard()
    else:
        kb = game_keyboard()
    await message.answer(
        "🍾❤️ <b>Spin the Bottle</b> o'yiniga xush kelibsiz!\n\n"
        "Shishani aylantiring, sovg'alar yuboring, Baxt g'ildiragini sinab ko'ring "
        "va do'stlaringiz bilan qiziqarli vaqt o'tkazing!\n\n"
        "Boshlash uchun quyidagi tugmani bosing 👇",
        reply_markup=kb,
        parse_mode="HTML",
    )


@dp.message(Command("admin"))
async def admin_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ Bu buyruq faqat admin uchun.")
        return
    await message.answer("⚙️ Admin panelga o'tish:", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Admin panelni ochish",
                                                web_app=WebAppInfo(url=f"{WEBAPP_URL}/admin"))]]
    ))


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "🍾 <b>Spin the Bottle</b>\n\n"
        "/start — o'yinni boshlash\n"
        "/help — yordam\n"
        + ("/admin — admin panel\n" if message.from_user.id == ADMIN_ID else ""),
        parse_mode="HTML",
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
