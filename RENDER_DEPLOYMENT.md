# 🚀 Render.com da Deploy Qilish Qo'llanmasi

## 🔧 Masalani Hal Qilish

### ❌ Xato Bo'ldi
```
ERROR: Could not find a version that satisfies the requirement aiosqlite==3.1.0
```

### ✅ Tuzatildi
```txt
requirements.txt da noto'g'ri versiyalar faqat!

❌ aiosqlite==3.1.0  ← BU VERSIYA MAVJUD EMas!
✅ aiosqlite==0.22.1 ← CORRECT VERSION
```

---

## 📝 Corrected requirements.txt

```txt
aiogram==3.4.1
aiosqlite==0.22.1
python-dotenv==1.0.0
aiohttp==3.9.1
```

**Muhim**: `asyncio==3.4.3` ni o'chirib tashladim chunki u Python-ga built-in!

---

## 🎯 Render.com da Deploy Qilish (Step-by-Step)

### 1-qadam: GitHub Repository

#### A) Repository yaratish
```bash
git init smm_master_bot
cd smm_master_bot
git add .
git commit -m "Initial commit"
git push origin main
```

#### B) .gitignore tekshiruvi
```
.env
*.db
logs/
backups/
venv/
__pycache__/
*.pyc
```

#### C) Repoga push qilish
```bash
git remote add origin https://github.com/YOURUSERNAME/smm-master-bot.git
git branch -M main
git push -u origin main
```

---

### 2-qadam: Render.com da Service Yaratish

#### A) Login qiling
1. https://render.com ga kiring
2. GitHub-da sign up qiling

#### B) Yangi Service yaratish
1. "New +" tugmasini bosing
2. "Web Service" ni tanlang
3. GitHub repository-ni tanlang
4. "smm-master-bot" (yoki sizning repo nomi)

#### C) Configuration

**Name:**
```
smm-master-bot
```

**Environment:**
```
Python 3.11.9  ← IMPORTANT! NOT 3.14!
```

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
python main.py
```

**Environment Variables** qo'shing:
```
MASTER_BOT_TOKEN = 8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg
ADMIN_ID = 7861165622
PYTHON_VERSION = 3.11.9
```

⚠️ **CRITICAL**: Python version 3.11.9 tanlang (3.14 ishlamaydi)

---

### 3-qadam: Konfiguratsiya Sozlash

#### A) Render.yaml yaratish (optional)

Proyektning root-da `render.yaml` yarating:

```yaml
services:
  - type: web
    name: smm-master-bot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: MASTER_BOT_TOKEN
        value: 8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg
      - key: ADMIN_ID
        value: "7861165622"
```

#### B) Procfile yaratish (optional)

```
worker: python main.py
```

---

## 🐧 Agar VPS/Linux Server-da Deploy Qilmoqchi Bo'lsangiz

### Recommended: DigitalOcean yoki Linode

#### 1. SSH orqali server ga ulanish
```bash
ssh root@YOUR_SERVER_IP
```

#### 2. Dependencies o'rnatish
```bash
apt update
apt install python3.11 python3-pip git screen
```

#### 3. Repository clone qilish
```bash
cd /home
git clone https://github.com/YOURUSERNAME/smm-master-bot.git
cd smm-master-bot
```

#### 4. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Environment variables
```bash
cp .env.example .env
nano .env
# Token va Admin ID ni kiriting
```

#### 6. Screen-da ishga tushirish
```bash
screen -S smm_bot
python main.py

# Ctrl+A, D orqali chiqish
```

#### 7. Bot holatini tekshirish
```bash
screen -list
screen -r smm_bot
```

---

## ☁️ Render.com-ning Bepul Plani Haqida

**Render-ning Free Plan:**
- ✅ Auto-deploys GitHub-dan
- ✅ Free domain
- ✅ Auto SSL
- ❌ Bepul deploy 7 kun ishlay digan qilib turamiz (sleep mode)
- ✅ Paid plan bo'lsa 24/7 ishlay turadi

**Agar 24/7 kere bo'lsa:**
1. Paid plan-ga o'ting (minimum $7/month)
2. Yoki VPS (DigitalOcean $5/month)

---

## 🔧 PYDANTIC-CORE XATOSI - YECHIM

### ❌ Xato Ko'rinishi
```
error: metadata-generation-failed
pydantic-core
Read-only file system (os error 30)
maturin failed
```

### ✅ YECHIM - 3 QADAM

#### 1️⃣ Python Versiyasini Tekshiring
```
Render Dashboard → Settings → Python Version
✅ Python 3.11.9 TANLANG
❌ Python 3.14 o'chirib tashlang
```

**WHY?** Python 3.14 (pre-release) - unstable!

#### 2️⃣ Build Command-ni Guncelleshtiring
```bash
# ❌ OLD
pip install -r requirements.txt

# ✅ NEW
pip install --upgrade pip && pip install -r requirements.txt
```

#### 3️⃣ Requirements.txt-ni Tekshiring
```txt
aiogram==3.4.1
aiosqlite==0.22.1
python-dotenv==1.0.0
aiohttp==3.9.1
pydantic==2.5.0          ← Stable version
pydantic-core==2.14.1    ← Pre-built wheels
typing-extensions==4.8.0 ← Dependency
```

### ⚡ Murakkab Bo'lsa: render.yaml Ishlatish

```bash
# Repository root-da quyidagi faylni yarating:
render.yaml
```

Mazmuni:
```yaml
services:
  - type: web
    name: smm-master-bot
    env: python
    pythonVersion: 3.11.9
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: python main.py
```

---

## ✅ Deploy Tekshiruvi

### Render Console-da Tekshirish

1. **Build Logs:**
   - "Logs" tabiga kiring
   - Nima degan qilganini ko'ring

2. **Deploy Status:**
   - "Deployments" tabiga kiring
   - Status ko'ring

3. **Test:**
   - Telegram: `/start` yuboring
   - Bot javob berishi kerak

### Xatolar Bo'lsa

**"Python version error":**
```yaml
buildCommand: pip install -r requirements.txt
# yoki
buildCommand: pip install --upgrade pip && pip install -r requirements.txt
```

**"Module not found":**
- requirements.txt-da to'g'ri versiyalar borligini tekshiring
- `pip freeze > requirements.txt` qilmang (venv-ning barcha paketlari yoziladi)

**"Connection timeout":**
- Internet ulanishi tekshiring
- Telegram API accessibility

---

## 🔐 Environment Variables Render-da

### Method 1: Render Dashboard-dan
```
Seting → Environment
MASTER_BOT_TOKEN = xxxxx
ADMIN_ID = 123456
```

### Method 2: render.yaml-dan
```yaml
envVars:
  - key: MASTER_BOT_TOKEN
    value: xxxxx
  - key: ADMIN_ID
    value: "123456"
```

### Method 3: .env fayldan (NOT RECOMMENDED)
```
# .env-ni repo-ga push qilmang!
```

---

## 📊 Database Render-da

**SQLite problemi:**
- Render ephemeral file system ishlatadi
- Bot restartdan keyin database o'chib ketadi

**Yechim: PostgreSQL ishlatish**

### PostgreSQL Setup

1. **Render-da Postgres qo'shish**
   - Dashboard → "New +" → "PostgreSQL"
   - Min plani tanlang

2. **requirements.txt-ga qo'shish**
```txt
psycopg2-binary==2.9.9
```

3. **config.py-da o'zgartirish**
```python
# SQLite o'rniga:
DATABASE_URL = os.getenv("DATABASE_URL")
# psycopg2 ishlatish
```

---

## 🎯 Optimal Setup Render-da

### Architecture
```
┌─────────────────────────────────┐
│   Render.com                    │
├─────────────────────────────────┤
│  Web Service (SMM Master Bot)   │
│  - Python 3.11                  │
│  - Auto-deploy GitHub-dan       │
├─────────────────────────────────┤
│  PostgreSQL Database (optional)  │
│  - Persistent storage           │
│  - Paid plan: $15/month         │
└─────────────────────────────────┘
```

### Cost Estimate
- Free: $0 (7 kun ishlay turadi)
- Paid (24/7): $7-15/month
- + Database: $15/month

---

## 🚀 Deploy Muvaffaqiyat Tekshiruvi

### Green Light ✅
```
✅ Build succeeded
✅ Service is live
✅ Logs ko'rinmoqda
✅ Telegram: Bot javob bermoqda
✅ /admin ishlamoqda
```

### Red Light ❌
```
❌ Build failed - requirements.txt tekshiring
❌ Service crashed - logs ko'ring
❌ Telegram javob bermaydi - token tekshiring
❌ Database xatosi - PostgreSQL sozlang
```

---

## 📞 Troubleshooting

### "Build failed" xatosi
```bash
# Local-da tekshiring:
python -m pip install -r requirements.txt

# Agar local-da OK bo'lsa:
# Render-ning Python versiyasini tekshiring
```

### "Service stopped" xatosi
```bash
# Render logs-iga qaring
# Adatdan start command tekshiring
```

### "Deployment is taking too long"
- Render bepul plan-da 15 minutdan o'ziq ishlamaydi
- Paid plan oling yoki timeout-ni ko'payitring

---

## 💾 GitHub Push Qilish

Har gal yangilash kerak bo'lsa:

```bash
git add .
git commit -m "Update SMM features"
git push origin main

# Render avtomatik deploy qiladi! 🚀
```

---

## 📌 Checklist

Deploy-dan oldin:

- [ ] requirements.txt to'g'ri versiyalar bor
- [ ] .env-da token va Admin ID
- [ ] GitHub repository-ga push qilindi
- [ ] Render-da GitHub tanlandi
- [ ] Start command to'g'ri: `python main.py`
- [ ] Environment variables kiriting
- [ ] Database sozlamalari (agar postgres kerak bo'lsa)

---

## 🎉 Tayyor!

Endi deploy qiling va botingiz cloud-da ishlay boshlaydi! ☁️

```bash
# GitHub-ga push qiling
git push origin main

# Render avtomatik deploy qiladi
# ~2-3 minut-dan keyin live bo'ladi 🚀
```

---

## 💡 Pro Tips

1. **Free plan-dan Paid-ga o'tish:**
   - Dashboard → Settings → Plan
   - Paid plan tanlang ($7+)

2. **Database persistent qilish:**
   - PostgreSQL qo'shish (Render-da free yok)
   - Yoki Supabase (free PostgreSQL)

3. **Auto-restart:**
   - Cron job o'rniga Render-ning "Scheduler" ishlatish

4. **Monitoring:**
   - Telegram xabar yuboring
   - Status bot setup qiling

---

## 📚 Qo'shimcha Resurslar

- [Render Docs](https://render.com/docs)
- [Python Deployment](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Databases on Render](https://render.com/docs/databases)

---

**Sukses bo'ling! Cloud-da ishlayotgan bot! ☁️🚀**
