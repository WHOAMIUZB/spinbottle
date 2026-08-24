"""
Configuration file for SMM Master Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
MASTER_BOT_TOKEN = os.getenv("MASTER_BOT_TOKEN", "8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7861165622"))

# Database
DB_PATH = "smm_master.db"
DB_BACKUP_PATH = "backups/"

# Features
ENABLE_REFERRAL_SYSTEM = True
ENABLE_PROMO_CODES = True
ENABLE_VIP_SYSTEM = True
ENABLE_SCHEDULED_MESSAGES = True
ENABLE_WHITE_LIST = True
ENABLE_ANALYTICS = True

# API Limits
MAX_BROADCAST_SIZE = 1000  # users per broadcast
MAX_API_KEYS = 50
MAX_BOT_TOKENS = 100

# Pricing
DEFAULT_API_PRICE = 0.5  # USD
REFERRAL_BONUS_PERCENT = 10
VIP_MONTHLY_PRICE = 9.99

# Message Templates
WELCOME_MESSAGE = """
🤖 <b>SMM Master Bot</b> xush kelibsiz!

Nima qila olasiz:
✅ Xizmatlarni sotib olish
✅ Promo kodlarni qo'llash
✅ Statistika ko'rish
✅ API larni boshqarish

/help - To'liq ma'lumot
"""

ADMIN_WELCOME = """
🔐 <b>SMM Master Bot - Admin Panel</b>

Xush kelibsiz, Admin!

Imkoniyatlar:
✅ Ko'plab bot tokenlarini boshqarish
✅ API kalitlarini qo'shish/o'chirish
✅ Broadcast xabarlar yuborish
✅ Promo kodlar yaratish
✅ Foydalanuvchilarni boshqarish
✅ Tola statistika
✅ Backup yaratish

/admin - Admin panel
"""

# Admin Warnings
ADMIN_COMMANDS = [
    "add_bot", "remove_bot", "add_api", "remove_api",
    "send_broadcast", "ban_user", "unban_user",
    "create_promo", "view_logs", "backup_database"
]

# Logging
LOG_FILE = "logs/smm_master.log"
LOG_LEVEL = "INFO"

# Timezone
TIMEZONE = "Asia/Tashkent"

# Rate Limiting
RATE_LIMIT_BROADCAST = 5  # messages per minute
RATE_LIMIT_API = 100  # requests per minute

# Features List (30+ Features)
FEATURES = {
    "bot_management": {
        "add_bot": "Bot token qo'shish",
        "remove_bot": "Botni o'chirish",
        "list_bots": "Barcha botlarni ko'rish",
        "bot_stats": "Bot statistikasi",
        "bot_health_check": "Bot holatini tekshirish"
    },
    "api_management": {
        "add_api": "API kaliti qo'shish",
        "remove_api": "API kalitini o'chirish",
        "list_apis": "Barcha API larni ko'rish",
        "update_price": "API narxini o'zgartirish",
        "test_api": "API ni sinab ko'rish",
        "api_usage_stats": "API foydalanish statistikasi"
    },
    "broadcast": {
        "broadcast_text": "Matn xabari yuborish",
        "broadcast_image": "Rasm yuborish",
        "broadcast_video": "Video yuborish",
        "schedule_broadcast": "Xabarni jadvallash",
        "broadcast_stats": "Broadcast statistikasi",
        "broadcast_analytics": "Broadcast analitikasi"
    },
    "user_management": {
        "ban_user": "Foydalanuvchini bloklash",
        "unban_user": "Bloklanishi ochiladigan user",
        "user_analytics": "User analitikasi",
        "view_user_info": "User ma'lumoti ko'rish",
        "bulk_import": "Ko'p foydalanuvchini import",
        "white_list": "White list yaratish"
    },
    "promo_system": {
        "create_promo": "Promo kod yaratish",
        "apply_promo": "Promo kodini qo'llash",
        "promo_stats": "Promo statistikasi",
        "discount_coupon": "Chegirma kupon",
        "bulk_promo": "Ko'p promo yaratish"
    },
    "referral_system": {
        "generate_referral": "Referral link yaratish",
        "referral_stats": "Referral statistikasi",
        "referral_payout": "Referral to'lovi",
        "referral_analytics": "Referral analitikasi"
    },
    "analytics": {
        "dashboard": "Asosiy statistika",
        "performance_report": "Performance report",
        "revenue_analytics": "Daromad analitikasi",
        "user_behavior": "User xatti-harakati",
        "export_data": "Ma'lumotni export qilish"
    },
    "settings": {
        "general_settings": "Umumiy sozlamalar",
        "pricing_settings": "Narx sozlamalari",
        "message_templates": "Xabar shablonlari",
        "system_backup": "Sistemani ehtiyotlash",
        "logs_viewer": "Loglarni ko'rish"
    }
}

# Total Features Count
TOTAL_FEATURES = sum(len(v) for v in FEATURES.values())

print(f"🎯 Jami funksiyalar: {TOTAL_FEATURES}")
