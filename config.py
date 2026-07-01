import os

# ==== ASOSIY SOZLAMALAR ====
BOT_TOKEN = os.getenv("BOT_TOKEN", "7998435200:AAHW4a-WXj2aVmBwb8s0bSTA4jeBYzjbFQg")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7861165622"))
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "spinbottle.db"))

# Mini App joylashgan (deploy qilingan) domen manzili.
# Buni Render/Railway/VPS ga deploy qilgandan keyin haqiqiy https manzil bilan almashtiring.
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.example.com")

# Web brauzerda (Telegramsiz) admin panelga standalone kirish uchun parol.
# Ishlab chiqarishda buni albatta o'zgartiring / environment variable orqali bering!
ADMIN_PANEL_SECRET = os.getenv("ADMIN_PANEL_SECRET", "admin7861165622")

# FastAPI serverni qaysi portda ishga tushirish
PORT = int(os.getenv("PORT", "8000"))
