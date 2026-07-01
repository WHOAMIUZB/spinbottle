# 🍾❤️ Spin the Bottle — Telegram Mini App

To'liq funksional "Spin the Bottle" (Shishani aylantirish) o'yini — web (Telegram Mini App)
ko'rinishida, `@spinthe_bot` uslubida, **to'liq admin panel** bilan.

## 📦 Loyihada nima bor

```
spinbottle/
  app.py              — FastAPI server: o'yin API + admin API + WebSocket (real vaqt)
  bot.py              — Telegram bot (aiogram 3.x): /start orqali Mini App tugmasini yuboradi
  bot_broadcast.py    — Admin panel orqali ommaviy xabar yuborish
  database.py         — aiosqlite: barcha jadvallar va CRUD funksiyalar
  telegram_auth.py    — Telegram WebApp initData ni HMAC orqali tekshirish (xavfsizlik)
  config.py           — Sozlamalar (BOT_TOKEN, ADMIN_ID va h.k.)
  requirements.txt
  static/
    index.html / css/style.css / js/app.js     — O'yinning o'zi (Mini App)
    admin.html / css/admin.css / js/admin.js   — Admin panel
```

## 🎮 O'yinda mavjud funksiyalar (skrinshotlaringizga mos)

- ❤️ Hearts balansi va uni ko'rsatuvchi panel
- 🪑 Stol atrofida o'tirgan foydalanuvchilar (avatarlar, VIP belgisi)
- 🍾 Shishani aylantirish — tasodifiy 2 kishi tanlanadi, natija animatsiyasi bilan
- 💬 Real vaqt chat (WebSocket orqali)
- 🎁 Sovg'a/reaksiya yuborish — har birining o'z narxi (❤️) va qabul qiluvchiga beriladigan bali bor
- 💗 Do'kon — hearts paketlari (Telegram Stars ⭐ narxida), VIP status, bonuslar
- 🎁 Bepul hearts — do'st taklif qilish, kanalga obuna, kompliment
- 🎡 Baxt g'ildiragi — tasodifiy sovg'alar, "Шансы" (bepul aylanishlar)
- ⚙️ Sozlamalar — ovoz/musiqa, profil, biz bilan bog'lanish

## 🛠️ Admin panelda mavjud funksiyalar

Admin **hammasini** o'zgartira oladi:

- 📊 **Statistika** — foydalanuvchilar soni, aylanmadagi hearts, VIP sони, so'nggi tranzaksiyalar
- 👥 **Foydalanuvchilar** — qidirish, hearts qo'shish/ayirish, VIP berish, bloklash
- 🎁 **Reaksiyalar** — **yangi reaksiya (emoji) qo'shish**, har biriga **narx va ball belgilash**, tahrirlash, faolsizlantirish, o'chirish
- 🎡 **Baxt g'ildiragi** — yangi sovg'a qo'shish, mukofot miqdori va tushish ehtimolini (weight) sozlash
- 💗 **Do'kon** — hearts paketlari, Stars narxi, bonus %, belgilar (Хит/Выгодно)
- 🪑 **Xonalar** — yangi stol/xona qo'shish
- 📢 **Ommaviy xabar** — barcha foydalanuvchilarga botdan xabar yuborish
- ⚙️ **Sozlamalar** — majburiy kanal, referral/obuna/kompliment bonuslari, g'ildirak narxi

Admin panelga kirish ikki xil usulda ishlaydi:
1. **Telegram orqali** — agar sizning Telegram ID'ingiz `ADMIN_ID` bilan mos bo'lsa, avtomatik kirasiz
2. **Web parol orqali** — brauzerda `ADMIN_PANEL_SECRET` parolini kiritib kirish mumkin (standalone test uchun)

## 🚀 1-bosqich: Lokal/serverda ishga tushirish (web holatda)

```bash
cd spinbottle
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Kutubxonalar o'rnatilgach serverni ishga tushiring:
uvicorn app:app --host 0.0.0.0 --port 8000
```

Brauzerda oching:
- O'yin: `http://localhost:8000/?dev_user_id=111` (Telegram tashqarisida test uchun `dev_user_id` ishlatiladi)
- Admin panel: `http://localhost:8000/admin` — parolni kiriting: `admin7861165622`
  (buni `config.py` dagi `ADMIN_PANEL_SECRET` orqali o'zgartirishingiz mumkin)

> DEV rejimda `dev_user_id` — bu faqat Telegramsiz sinash uchun. Ishlab chiqarishda
> (production) bu oddiy `?dev_user_id=` parametri **butunlay ishlatilmaydi**, chunki
> Telegram avtomatik ravishda xavfsiz `initData` yuboradi.

## 🌐 2-bosqich: Internetga chiqarish (deploy)

Botni Telegram bilan ulash uchun serveringiz **https** manzilga ega bo'lishi kerak
(Telegram Mini App faqat https bilan ishlaydi). Bepul variantlardan biri:

### Render.com orqali (tavsiya etiladi)
1. Loyihani GitHub repo'ga yuklang
2. Render.com da "Web Service" yarating, shu repo'ni ulang
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Environment Variables bo'limida qo'shing:
   - `BOT_TOKEN` = sizning bot tokeningiz
   - `ADMIN_ID` = `7861165622`
   - `ADMIN_PANEL_SECRET` = o'zingiz xohlagan kuchli parol
   - `WEBAPP_URL` = Render sizga bergan `https://...onrender.com` manzili
6. Deploy tugagach, `config.py`dagi (yoki environment variable orqali) `WEBAPP_URL`ni
   aniq shu manzilga o'rnating.

### Railway.app, Fly.io, yoki oddiy VPS orqali ham xuddi shunday tartibda ishlaydi
— asosiysi: `uvicorn app:app` https orqali internetga ochiq bo'lishi kerak.

## 🤖 3-bosqich: Botga ulash

1. `WEBAPP_URL`ni haqiqiy https manzilingizga o'rnating (`config.py` yoki environment variable)
2. BotFather orqali botingizga Menu Button qo'shishingiz mumkin (ixtiyoriy):
   `/setmenubutton` → botni tanlang → tugma nomi va `WEBAPP_URL`ni kiriting
3. Botni ishga tushiring (bu alohida, doimiy ishlaydigan process bo'lishi kerak):

```bash
python3 bot.py
```

4. Botga `/start` yozing — "🍾 O'ynash" tugmasi chiqadi, bosilganda Mini App ochiladi
5. Agar siz (`ADMIN_ID=7861165622`) botga yozsangiz, qo'shimcha "⚙️ Admin panel" tugmasi
   ham chiqadi va `/admin` buyrug'i orqali ham ochish mumkin

> **Eslatma:** `app.py` (web server) va `bot.py` (Telegram bot) — ikkalasi ham **bir vaqtda,
> alohida process sifatida** doimiy ishlab turishi kerak. Masalan Render'da ikkita
> "Web Service"/"Background Worker" yarating: biri `app.py` uchun, ikkinchisi `bot.py` uchun.

## 🔒 Xavfsizlik bo'yicha muhim eslatma

Siz yuborgan bot tokeni ushbu suhbatda ochiq matnda ko'rindi. Tavsiya:
- Tokenni ishlab chiqarishda **environment variable** (`BOT_TOKEN`) orqali bering,
  kodga yoki repo'ga yozib qo'ymang
- Agar token allaqachon boshqalar ko'rgan bo'lishi ehtimoli bo'lsa, BotFather'da
  `/revoke` orqali eskisini bekor qilib, yangi token oling
- `ADMIN_PANEL_SECRET`ni albatta murakkab parolga almashtiring

## 💳 To'lovlar haqida (Telegram Stars)

Do'kon bo'limi hozircha demo rejimda ishlaydi (frontend orqali). Haqiqiy to'lovni yoqish uchun:
1. Backend'da Telegram Bot API'ning `createInvoiceLink` / `answerPreCheckoutQuery` /
   `successful_payment` funksiyalarini `bot.py`ga qo'shish kerak (Stars uchun `XTR` valyuta)
2. `app.js`dagi `buyPackage()` funksiyasini `tg.openInvoice()` chaqiruvi bilan to'liq ulash kerak

Bu qism xavfsizlik va real pul/Stars aylanishi bilan bog'liq bo'lgani uchun ataylab asosiy
demo tuzilmadan alohida qoldirildi — xohlasangiz buni ham keyingi bosqichda to'liq ulab beraman.

## 🧩 Ma'lumotlar bazasini boshqarish

Barcha ma'lumotlar `spinbottle.db` (SQLite) faylida saqlanadi, birinchi ishga tushganda
avtomatik yaratiladi va standart reaksiyalar/sovg'alar/paketlar bilan to'ldiriladi (seed).
