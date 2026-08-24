# 🚀 SMM Master Bot - Professional Management System

**30+ funksiyali Telegram bot management sistema**

## 📋 Xususiyatlar (30+ Features)

### 🤖 Bot Management (5 features)
- ✅ Bot token qo'shish
- ✅ Botni o'chirish
- ✅ Barcha botlarni ko'rish
- ✅ Bot statistikasi
- ✅ Bot holatini tekshirish

### 🔑 API Management (6 features)
- ✅ API kaliti qo'shish
- ✅ API kalitini o'chirish
- ✅ Barcha API larni ko'rish
- ✅ API narxini o'zgartirish
- ✅ API ni sinab ko'rish
- ✅ API foydalanish statistikasi

### 📢 Broadcast System (6 features)
- ✅ Matn xabari yuborish
- ✅ Rasm yuborish
- ✅ Video yuborish
- ✅ Xabarni jadvallash
- ✅ Broadcast statistikasi
- ✅ Broadcast analitikasi

### 👤 User Management (6 features)
- ✅ Foydalanuvchini bloklash
- ✅ Bloklanishi ochiladigan user
- ✅ User analitikasi
- ✅ User ma'lumoti ko'rish
- ✅ Ko'p foydalanuvchini import
- ✅ White list yaratish

### 🎟 Promo System (5 features)
- ✅ Promo kod yaratish
- ✅ Promo kodini qo'llash
- ✅ Promo statistikasi
- ✅ Chegirma kupon
- ✅ Ko'p promo yaratish

### 👥 Referral System (4 features)
- ✅ Referral link yaratish
- ✅ Referral statistikasi
- ✅ Referral to'lovi
- ✅ Referral analitikasi

### 📊 Analytics (5 features)
- ✅ Asosiy statistika dashboard
- ✅ Performance report
- ✅ Daromad analitikasi
- ✅ User xatti-harakati
- ✅ Ma'lumotni export qilish

### ⚙️ Settings (5 features)
- ✅ Umumiy sozlamalar
- ✅ Narx sozlamalari
- ✅ Xabar shablonlari
- ✅ Sistemani ehtiyotlash
- ✅ Loglarni ko'rish

---

## 🛠 O'rnatish

### 1. Repository ni klonlash
```bash
git clone https://github.com/yourusername/smm-master-bot.git
cd smm-master-bot
```

### 2. Virtual Environment yaratish
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Dependencies o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Environment variables o'rnatish
`.env` fayl yaratish:
```env
MASTER_BOT_TOKEN=8703682072:AAFXt3dYiUabWXoopN6dmu7YQflZt2mYtRg
ADMIN_ID=7861165622
```

### 5. Botni ishga tushirish
```bash
python main.py
```

---

## 📚 Admin Buyruqlari

### Asosiy Buyruqlar
```
/start           - Botni boshlash
/admin           - Admin panelga kirish
/help            - Yordam menyu
/broadcast       - Xabar yuborish
/bots            - Barcha botlar
/apis            - Barcha APIlar
```

### Admin Panel Tugmalari
- 🤖 **Bot Qo'shish** - Yangi bot token qo'shish
- 🗑 **Bot O'chirish** - Mavjud botni o'chirish
- 🔑 **API Qo'shish** - API kaliti qo'shish
- 📊 **API Ro'yxat** - Barcha APIlarni ko'rish
- 📢 **Broadcast Yuborish** - Xabar broadcast
- ⏱ **Xabar Jadvali** - Vaqtinchalik xabar
- 🎟 **Promo Yaratish** - Promo kod yaratish
- 👤 **User Ban** - Foydalanuvchini bloklash
- 📈 **Statistika** - Tola statistika
- ⚙️ **Sozlamalar** - System sozlamalari

---

## 📊 Database Struktura

### Jadvallar (8 ta)

1. **bot_tokens** - Bot tokenlarini saqlash
2. **api_keys** - API kalitlarini saqlash
3. **users** - Foydalanuvchilar ma'lumoti
4. **broadcasts** - Broadcast loglar
5. **promo_codes** - Promo kodlar
6. **settings** - System sozlamalari
7. **statistics** - Statistika loglar
8. **scheduled_messages** - Jadvallangan xabarlar

### Qo'shimcha Jadvallar (auto-create)
- `white_lists` - White list
- `user_discounts` - User chegirmalar
- `custom_packages` - Custom paketlar
- `balance_history` - Balans tarix
- `announcements` - Elonlar
- `system_logs` - System loglar

---

## 🔐 Xavfsizlik

- ✅ Admin ID tekshiruvi
- ✅ Token validation
- ✅ User ban sistema
- ✅ White list funktsionalligi
- ✅ Database encryption (qo'shimcha)

---

## 📈 Statistika Ko'rish

### Admin Dashboard
```
👥 Jami foydalanuvchilar: 1,234
📨 Jami xabarlar: 56,789
🤖 Faol botlar: 15
🔑 API ishlatilishi: 123,456
```

### Bot bo'yicha Statistika
```
🤖 Bot Nomi
👥 1,234 users
💬 56,789 messages
📅 Qo'shilgan: 2024-01-15
```

---

## 🎁 Promo Sistema

### Promo Kod Yaratish
```
Kod: PROMO2024
Chegirma: 20%
Max foydalanish: 1000
Tugash: 2099-12-31
```

### Qo'llash
```
/promo PROMO2024
```

---

## 👥 Referral Sistema

### Referral Link
```
https://t.me/bot?start=ABC12345
```

### Bonus
- 10% har bir referral
- Unlimited referrals
- Auto payout

---

## 🗄 API Management

### API Qo'shish
```
Nomi: OpenAI GPT-4
Kalit: sk-...
Narxi: $0.005 per request
Kategoriya: Text Generation
```

### Narx O'zgartirish
- Admin panel orqali
- Real-time updates
- Auto sync barcha botlarga

---

## 📤 Broadcast Xabarlar

### Turlar
1. **Matn Xabari** - Simple text
2. **Rasm** - Image + caption
3. **Video** - Video + description

### Jadvallash
```
Vaqt: 2024-02-01 10:00
Matn: Yangi xizmat!
Botlar: Barcha/Tanlangan
```

---

## 📊 Advanced Features

### 1. User Analytics
- Join tarix
- Total requests
- Balance tracking
- VIP status

### 2. Performance Report
- Daily/Weekly/Monthly
- New users
- Revenue
- Active users

### 3. Data Export
- User data
- Transaction history
- Statistics
- API usage

### 4. System Backup
- Auto backup
- Manual backup
- Restore functionality

### 5. Logging
- System logs
- User actions
- API calls
- Errors

---

## 🔄 Workflow Misoli

### Bot Qo'shish
```
1. /admin - Admin panelga kirish
2. 🤖 Bot Qo'shish tugmasi
3. Bot tokenini kiriting
4. Bot nomini kiriting
5. ✅ Bot qo'shildi!
```

### Broadcast Yuborish
```
1. /admin - Admin panelga kirish
2. 📢 Broadcast Yuborish tugmasi
3. Xabar turini tanlang
4. Xabar matnini kiriting
5. ✅ Barcha botlarga yuborildi!
```

### Statistika Ko'rish
```
1. /admin - Admin panelga kirish
2. 📈 Statistika tugmasi
3. Tola statistikani ko'ring
4. Bot bo'yicha statistika
```

---

## 🚨 Xatonik Hal Qilish

### Database xatosi
```bash
rm smm_master.db
python main.py  # Re-initialize
```

### Token xatosi
```
❌ Noto'g'ri format! Token shaklini tekshiring.
```

Shaklni tekshiring: `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg`

### Admin xatosi
```
❌ Sizda ruxsat yo'q!
```

ADMIN_ID ni tekshiring `.env` faylda

---

## 📞 Qo'llab-quvvatlash

### Telegram
- [@admin_username](https://t.me/admin_username)

### Issues
- GitHub Issues orqali

### Suggest Features
- Pull requests ni oʻq!

---

## 📝 Litsenziya

MIT License - Bepul foydalanish

---

## 🎯 Roadmap

- [ ] Telegram Premium integration
- [ ] Mobile app
- [ ] Advanced AI features
- [ ] Payment integration
- [ ] Multi-language support
- [ ] API v2
- [ ] Advanced analytics

---

## 🙏 Rahmat!

Bu botdan foydalanganingiz uchun tashakkur!

**Yangi versiya**: v1.0.0
**Oxirgi o'zgarish**: 2024-01-15
**Davomiyligi**: Active Development

---

**Sukses bo'ling! 🚀**
