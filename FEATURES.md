# 🎯 SMM Master Bot - Barcha 30+ Funksiyalar

## 📖 Mundarija

1. [Bot Management](#bot-management)
2. [API Management](#api-management)
3. [Broadcast System](#broadcast-system)
4. [User Management](#user-management)
5. [Promo System](#promo-system)
6. [Referral System](#referral-system)
7. [Analytics](#analytics)
8. [Advanced Features](#advanced-features)
9. [Settings](#settings)

---

## 🤖 Bot Management (5 Features)

### 1️⃣ Bot Token Qo'shish
**Funktsiya**: Yangi SMM bot tokenni sistemaga qo'shish
```
/admin → 🤖 Bot Qo'shish → Token kiriting → Bot nomini kiriting
```
**Xususiyatlar**:
- Multiple bot tokens
- Auto validation
- Database storage
- User count tracking

### 2️⃣ Botni O'chirish
**Funktsiya**: Faol botni deaktivatsiya qilish
```
/admin → 🗑 Bot O'chirish → Botni tanlang
```
**Xususiyatlar**:
- Soft delete (data preserved)
- Instant deactivation
- User notification (optional)

### 3️⃣ Barcha Botlarni Ko'rish
**Funktsiya**: Sistemadagi barcha botlarni ko'rsatish
```
/admin → 📊 Botlar ro'yxati
```
**Xususiyatlar**:
- List view
- Pagination
- Status indicator
- User count per bot

### 4️⃣ Bot Statistikasi
**Funktsiya**: Har bir botning statistikasini ko'rish
```
/admin → 📈 Statistika → Bot tanlash
```
**Xususiyatlar**:
- Daily/Weekly/Monthly stats
- User growth chart
- Message frequency
- Revenue tracking

### 5️⃣ Bot Holatini Tekshirish (Health Check)
**Funktsiya**: Botning connectivity va status ni tekshirish
```
/admin → ⚙️ Settings → Bot Health Check
```
**Xususiyatlar**:
- Ping test
- API connectivity
- Response time
- Error logging

---

## 🔑 API Management (6 Features)

### 6️⃣ API Kaliti Qo'shish
**Funktsiya**: Yangi API integratsiyani qo'shish
```
/admin → 🔑 API Qo'shish → API nomi, kalit, narx, kategoriya
```
**Xususiyatlar**:
- Multiple API support
- Price management
- Category organization
- Limit tracking

### 7️⃣ API Kalitni O'chirish
**Funktsiya**: API kalitini deaktivatsiya qilish
```
/admin → 📊 API Ro'yxat → API tanlash → O'chirish
```
**Xususiyatlar**:
- Soft delete
- Usage history preserved
- Archive functionality

### 8️⃣ Barcha APIlarni Ko'rish
**Funktsiya**: Sistemadagi barcha APIlarni ro'yxati
```
/admin → 📊 API Ro'yxat
```
**Xususiyatlar**:
- Sortable columns
- Filter by category
- Price display
- Usage statistics

### 9️⃣ API Narxini O'zgartirish
**Funktsiya**: API uchun yangi narxni sozlash
```
/admin → 📊 API Ro'yxat → API tanlash → Narxini o'zgartirish
```
**Xususiyatlar**:
- Real-time price update
- Historical price tracking
- Percentage change indicator
- Discount application

### 🔟 API ni Sinab Ko'rish (Test API)
**Funktsiya**: API connectivity va functionality ni tekshirish
```
/admin → ⚙️ Settings → Test API
```
**Xususiyatlar**:
- Connection test
- Response validation
- Latency measurement
- Error detection

### 1️⃣1️⃣ API Foydalanish Statistikasi
**Funktsiya**: API usage analytics va trends
```
/admin → 📈 Statistika → API Usage
```
**Xususiyatlar**:
- Daily/Weekly usage
- Top APIs ranking
- Growth trends
- Cost analysis

---

## 📢 Broadcast System (6 Features)

### 1️⃣2️⃣ Matn Xabari Yuborish
**Funktsiya**: Barcha botlarga text broadcast
```
/admin → 📢 Broadcast → 📝 Matn → Matnni kiriting → Yuborish
```
**Xususiyatlar**:
- Rich text formatting
- HTML support
- Emoji support
- Preview before sending

### 1️⃣3️⃣ Rasm Xabari Yuborish
**Funktsiya**: Barcha botlarga image broadcast
```
/admin → 📢 Broadcast → 🖼 Rasm → Rasmni yuboring → Yuborish
```
**Xususiyatlar**:
- Image upload
- Caption support
- Compression optimization
- Format validation

### 1️⃣4️⃣ Video Xabari Yuborish
**Funktsiya**: Barcha botlarga video broadcast
```
/admin → 📢 Broadcast → 🎥 Video → Videoni yuboring → Yuborish
```
**Xususiyatlar**:
- Video upload
- Duration tracking
- Thumbnail support
- Quality optimization

### 1️⃣5️⃣ Xabar Jadvallash
**Funktsiya**: Broadcast xabarini kelajakda yuborish
```
/admin → ⏱ Xabar Jadvali → Vaqtni tanlang → Matn → Yuborish
```
**Xususiyatlar**:
- Schedule editor
- Time zone support
- Recurring options
- Cancellation support

### 1️⃣6️⃣ Broadcast Statistikasi
**Funktsiya**: Broadcast qilgan xabarlarning statistikasi
```
/admin → 📈 Statistika → Broadcast Stats
```
**Xususiyatlar**:
- Send success rate
- Delivery time tracking
- Failed delivery logging
- User engagement metrics

### 1️⃣7️⃣ Broadcast Analitikasi (Advanced)
**Funktsiya**: Detailed broadcast analytics
```
/admin → 📊 Analytics → Broadcast Analysis
```
**Xususiyatlar**:
- Click tracking
- Open rates
- Device analytics
- Geographic data

---

## 👤 User Management (6 Features)

### 1️⃣8️⃣ Foydalanuvchini Bloklash
**Funktsiya**: User account ni deaktivatsiya qilish
```
/admin → 👤 User Ban → User ID → Confirm
```
**Xususiyatlar**:
- Instant blocking
- Reason logging
- Automatic notification
- Reactivation option

### 1️⃣9️⃣ Bloklanishi Ochiladigan User
**Funktsiya**: Bloklangan userni qayta aktivatsiya qilish
```
/admin → 👤 User Unban → User ID → Confirm
```
**Xususiyatlar**:
- Unban confirmation
- Action logging
- Notification to user
- Re-access restoration

### 2️⃣0️⃣ User Analitikasi
**Funktsiya**: Barcha userning behavior analytics
```
/admin → 📈 Statistika → User Analytics
```
**Xususiyatlar**:
- Activity tracking
- Spending analytics
- Usage patterns
- Churn prediction

### 2️⃣1️⃣ User Ma'lumoti Ko'rish
**Funktsiya**: Specific user uchun detailed ma'lumot
```
/admin → 👤 User Info → User ID → View
```
**Xususiyatlar**:
- Profile information
- Transaction history
- Activity log
- Contact details

### 2️⃣2️⃣ Ko'p Foydalanuvchini Import (Bulk Import)
**Funktsiya**: CSV yoki JSON dan users import qilish
```
/admin → ⚙️ Settings → Bulk Import → File upload
```
**Xususiyatlar**:
- Batch processing
- Duplicate detection
- Error reporting
- Progress tracking

### 2️⃣3️⃣ White List Yaratish
**Funktsiya**: VIP/premium users uchun white list
```
/admin → ⚙️ Settings → White List → Add Users
```
**Xususiyatlar**:
- List management
- Multiple lists support
- Priority access
- Special features

---

## 🎟 Promo System (5 Features)

### 2️⃣4️⃣ Promo Kod Yaratish
**Funktsiya**: Discount promo code yaratish
```
/admin → 🎟 Promo Yaratish → Kod → Chegirma → Max Uses
```
**Xususiyatlar**:
- Custom code generation
- Discount percentage
- Usage limits
- Expiration date

### 2️⃣5️⃣ Promo Kodini Qo'llash
**Funktsiya**: Promo kodini user hesabida qo'llash
```
User: /promo PROMO2024
```
**Xususiyatlar**:
- Validation check
- Auto application
- Balance update
- Confirmation message

### 2️⃣6️⃣ Promo Statistikasi
**Funktsiya**: Promo codes performance metrics
```
/admin → 📈 Statistika → Promo Stats
```
**Xususiyatlar**:
- Usage tracking
- Revenue impact
- Popular codes
- Effectiveness report

### 2️⃣7️⃣ Chegirma Kupon (Coupon)
**Funktsiya**: One-time use discount coupons
```
/admin → 🎟 Coupon → Generate → Distribute
```
**Xususiyatlar**:
- Single use codes
- Amount-based discounts
- Expiration tracking
- Audit trail

### 2️⃣8️⃣ Ko'p Promo Yaratish (Bulk Promo)
**Funktsiya**: Bir vaqtda ko'p promo kodlarini yaratish
```
/admin → 🎟 Bulk Promo → Count → Template
```
**Xususiyatlar**:
- Batch generation
- Template-based
- Auto distribution
- Export options

---

## 👥 Referral System (4 Features)

### 2️⃣9️⃣ Referral Link Yaratish
**Funktsiya**: Unique referral link yaratish
```
/referral → Generate Link
Natija: https://t.me/bot?start=ABC12345
```
**Xususiyatlar**:
- Unique code generation
- QR code support
- Link tracking
- Shortened URL

### 3️⃣0️⃣ Referral Statistikasi
**Funktsiya**: Referral performance tracking
```
/referral → Stats
```
**Xususiyatlar**:
- Referred users count
- Total earnings
- Commission tracking
- Payment history

### 3️⃣1️⃣ Referral To'lovi (Payout)
**Funktsiya**: Referral earnings ni withdraw qilish
```
/referral → Withdraw → Amount → Confirm
```
**Xususiyatlar**:
- Payment processing
- Multiple payment methods
- Tax calculation
- Transaction history

### 3️⃣2️⃣ Referral Analitikasi (Advanced)
**Funktsiya**: Detailed referral analytics
```
/admin → 📊 Analytics → Referral Analysis
```
**Xususiyatlar**:
- Conversion tracking
- Lifetime value
- Tier-based bonuses
- Fraud detection

---

## 📊 Analytics (5 Features)

### 3️⃣3️⃣ Asosiy Statistika Dashboard
**Funktsiya**: Main statistics overview
```
/admin → 📈 Statistika
```
**Xususiyatlar**:
- Total users
- Total messages
- Active bots
- API usage
- Revenue summary

### 3️⃣4️⃣ Performance Report
**Funktsiya**: Comprehensive performance analysis
```
/admin → 📊 Reports → Performance
```
**Xususiyatlar**:
- Daily/Weekly/Monthly reports
- Growth metrics
- KPI tracking
- Trend analysis

### 3️⃣5️⃣ Daromad Analitikasi (Revenue Analytics)
**Funktsiya**: Financial metrics va revenue tracking
```
/admin → 💰 Revenue Analytics
```
**Xususiyatlar**:
- Total revenue
- Revenue by source
- Profit margins
- Forecasting

### 3️⃣6️⃣ User Xatti-Harakati (User Behavior)
**Funktsiya**: User behavior patterns analysis
```
/admin → 📊 Analytics → User Behavior
```
**Xususiyatlar**:
- Activity heatmap
- Peak hours
- Usage patterns
- Churn analysis

### 3️⃣7️⃣ Ma'lumotni Export Qilish (Export Data)
**Funktsiya**: Data export to CSV/Excel/PDF
```
/admin → ⚙️ Settings → Export Data → Format
```
**Xususiyatlar**:
- Multiple format support
- Scheduled exports
- Encrypted export
- Email delivery

---

## ⚙️ Advanced Features (5 Features)

### 3️⃣8️⃣ Umumiy Sozlamalar (General Settings)
**Funktsiya**: System-wide configuration
```
/admin → ⚙️ Settings → General
```
**Xususiyatlar**:
- Bot name/description
- Default timezone
- Language preference
- Notification settings

### 3️⃣9️⃣ Narx Sozlamalari (Pricing Settings)
**Funktsiya**: Price management across APIs
```
/admin → ⚙️ Settings → Pricing
```
**Xususiyatlar**:
- Default pricing
- Bulk discounts
- Tier-based pricing
- Currency settings

### 4️⃣0️⃣ Xabar Shablonlari (Message Templates)
**Funktsiya**: Pre-defined message templates
```
/admin → ⚙️ Settings → Templates
```
**Xususiyatlar**:
- Template library
- Custom variables
- Preview option
- Template reuse

### 4️⃣1️⃣ Sistemani Ehtiyotlash (System Backup)
**Funktsiya**: Database backup va restore
```
/admin → ⚙️ Settings → Backup → Create
```
**Xususiyatlar**:
- Auto backup schedule
- Manual backup
- Compression
- Cloud storage support

### 4️⃣2️⃣ Loglarni Ko'rish (Logs Viewer)
**Funktsiya**: System logs monitoring
```
/admin → ⚙️ Settings → Logs
```
**Xususiyatlar**:
- Real-time logging
- Log filtering
- Search functionality
- Log export

---

## 📌 Summary

| Kategoriya | Funksiyalar | Total |
|-----------|-------------|-------|
| Bot Management | 5 | 5 |
| API Management | 6 | 11 |
| Broadcast | 6 | 17 |
| User Management | 6 | 23 |
| Promo System | 5 | 28 |
| Referral System | 4 | 32 |
| Analytics | 5 | 37 |
| Advanced | 5 | 42 |

**Jami: 42+ funksiya!**

---

## 🚀 Ishlatish Qo'llanmasi

### Har kuni foydalaniladigan Features
1. Bot Management - Yangi bot qo'shish
2. Broadcast System - Xabarlari yuborish
3. Analytics - Statistika ko'rish

### Haftalik Tasks
1. API Management - Narxlarni tekshirish
2. User Management - Spam users o'chirish
3. Promo System - Yangi promo yaratish

### Oylik Tasks
1. Performance Report - Bugungi oyi report
2. Backup - Database backup
3. Revenue Analytics - Daromad analitikasi

---

## 💡 Pro Tips

1. **Batch Operations** - Ko'p users uchun promo yaratish
2. **Scheduling** - Optimal vaqtda broadcast yuborish
3. **Analytics** - Regular analytics tekshirish
4. **Security** - Muntazam password o'zgartirish
5. **Backup** - Haftalik backup yaratish

---

**Barcha funksiyalarni ishlatish uchun `/admin` buyrugi yuboring!** 🎯
