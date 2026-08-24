# 📦 O'rnatish va Sozlash Qo'llanmasi

## 🚀 Tez O'rnatish (5 minut)

### 1-qadam: Prerequisites
Kompyuteringizda quyidagilar o'rnatilgan bo'lishi kerak:
- Python 3.8+ 
- pip (Python package manager)
- Git (optional)

### 2-qadam: Fayllarni yuklab olish

**Option A: ZIP dan**
```bash
# ZIP ni extract qiling
unzip smm_master_bot.zip
cd smm_master_bot
```

**Option B: Git dan**
```bash
git clone https://github.com/yourusername/smm-master-bot.git
cd smm-master-bot
```

### 3-qadam: Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4-qadam: Dependencies o'rnatish
```bash
pip install -r requirements.txt
```

### 5-qadam: Environment sozlash

`.env.example` ni `.env` ga nomi o'zgartiring:
```bash
cp .env.example .env
```

`.env` faylda:
```env
MASTER_BOT_TOKEN=8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg
ADMIN_ID=7861165622
```

### 6-qadam: Botni ishga tushirish

```bash
python main.py
```

✅ **Bot muvaffaqiyatli ishga tushdi!**

---

## 📝 Bot Tokenini Olish

### 1. BotFather dan token olish

Telegram da `@BotFather` botini izlang:

1. `/start` buyrugi yuboring
2. `/newbot` buyrugi yuboring
3. Bot nomini kiriting (masalan: `SMM Master Bot`)
4. Foydalanuvchi nomini kiriting (masalan: `smm_master_bot`)
5. 🎉 Token olib olasiz!

Token ko'rinishi:
```
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
```

### 2. Admin ID ni olish

Telegram da `@userinfobot` botini yuboring:
- U sizning ID sini aytadi

---

## 🔧 Konfiguratsiya

### config.py faylida o'zgartirishlar

```python
# Master Bot Token
MASTER_BOT_TOKEN = "sizning_token"

# Admin ID
ADMIN_ID = 123456789

# Database
DB_PATH = "smm_master.db"

# Features
ENABLE_REFERRAL_SYSTEM = True
ENABLE_PROMO_CODES = True
ENABLE_VIP_SYSTEM = True
```

### .env faylida o'zgartirishlar

```env
MASTER_BOT_TOKEN=sizning_token
ADMIN_ID=123456789
LOG_LEVEL=INFO
TIMEZONE=Asia/Tashkent
```

---

## 📂 Fayl Strukturasi

```
smm_master_bot/
├── main.py                  # Asosiy bot fayli
├── database.py              # Database funksiyalari
├── config.py                # Konfiguratsiya
├── broadcast_manager.py     # Broadcast sistema
├── smm_features.py          # 30+ advanced features
├── utils.py                 # Yordamchi funksiyalar
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables example
├── README.md                # README
├── SETUP.md                 # O'rnatish qo'llanmasi (shu fayl)
└── logs/                    # Log fayllar (auto-create)
    └── smm_master.log
```

---

## 🐛 Xatonik Hal Qilish

### "Module not found" xatosi

```bash
pip install -r requirements.txt
```

### Bot ishlamayapti

Quyidagini tekshiring:
```bash
# Internet ulanishi
ping google.com

# Token to'g'riligi
python -c "from main import *"

# Python versiyasi
python --version  # 3.8+ bo'lishi kerak
```

### Database xatosi

```bash
# Database ni o'chirib qayta yaratish
rm smm_master.db
python main.py
```

### "Permission denied" xatosi

```bash
# Linux/Mac
chmod +x main.py

# Windows
# PowerShell dan Run Administrator sifatida
```

---

## 🔐 Xavfsizlik

### Muhim!
- `.env` faylni public repositoryga yuklamang
- Token va Admin ID ni hech kimga berishyabdi
- `.gitignore` da quyidagilarni qo'shing:

```
.env
*.db
logs/
backups/
*.pyc
__pycache__/
venv/
```

### Best Practices
- Muntazam backup yaratish
- Log fayllarni tekshirish
- Admin passwordlarini yaxshi saqlash
- SSL/HTTPS ishlatish (production)

---

## 🌐 Production Deploy

### Server da ishga tushirish

```bash
# 1. SSH orqali server ga ulanish
ssh user@server_ip

# 2. Fayllarni yuklash
git clone https://github.com/yourusername/smm-master-bot.git
cd smm-master-bot

# 3. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Dependencies
pip install -r requirements.txt

# 5. Environment setup
nano .env
# Token va Admin ID ni kiriting

# 6. Screen orqali ishga tushirish
screen -S smm_bot
python main.py

# Ctrl+A, D orqali chiqish (bot fonda ishlaydi)
```

### Systemd Service (Linux)

`/etc/systemd/system/smm-bot.service` faylini yarating:

```ini
[Unit]
Description=SMM Master Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/smm_master_bot
ExecStart=/home/your_user/smm_master_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ishga tushirish:
```bash
sudo systemctl start smm-bot
sudo systemctl enable smm-bot
sudo systemctl status smm-bot
```

---

## 📊 Database Backup

### Manual Backup

```bash
python -c "from smm_features import smm_features; smm_features.create_backup()"
```

### Auto Backup (Cron job)

```bash
# Har kuni 3:00 AM da backup yaratish
0 3 * * * cd /path/to/smm_master_bot && python -c "from smm_features import smm_features; smm_features.create_backup()"
```

---

## 📚 Keyingi Qadamlar

1. **Bot ma'lumotlarini o'rnatish**
   - `/admin` orqali admin panelga kirish
   - Birinchi bot tokenni qo'shish
   - API kalitlarini qo'shish

2. **Foydalanuvchilarni qo'shish**
   - Botni test qilish
   - White list yaratish
   - Referral linklar yaratish

3. **Promo kodlar**
   - Test promo yaratish
   - Foydalanuvchilarga tarqatish

4. **Monitoring**
   - Log fayllarni tekshirish
   - Statistikani monitoring qilish
   - Backup tekshiruvi

---

## 💡 Maslahatlar

### Performance
- Katta broadcast 1000+ users uchun jadvallash
- Database ni muntazam clean qilish
- API limit ni tekshirish

### Security
- HTTPS ishlatish
- Rate limiting ni sozlash
- Log fayllarni himoya qilish

### Scaling
- Multiple bot instances
- Database replication
- Caching qo'shish (Redis)

---

## 📞 Qo'llab-Quvvatlash

- **Issues**: GitHub Issues orqali
- **Telegram**: [@admin_username](https://t.me/admin_username)
- **Email**: admin@example.com

---

## ✅ Tekshiruv Ro'yxati

Botni ishga tushirishdan oldin:

- [ ] Token to'g'ri kiriting
- [ ] Admin ID to'g'ri kiriting
- [ ] Python 3.8+ o'rnatilgan
- [ ] Virtual environment faol
- [ ] Dependencies o'rnatilgan
- [ ] `.env` fayl yaratilgan
- [ ] Database initialize qilindi
- [ ] Logs direktori yaratilgan
- [ ] Backups direktori yaratilgan

---

## 🎉 Tayyor!

Endi botingiz ishlashga tayyor!

```bash
python main.py
```

Telegram da `/admin` buyrugi yuboring va management panelni ko'ring.

**Sukses bo'ling! 🚀**
