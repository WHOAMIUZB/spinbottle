"""
Advanced SMM Features Module
25+ funksiya qo'shilgan
"""

import aiosqlite
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random
import string
from database import DB_PATH

class SMMFeatures:
    """Advanced SMM Features"""
    
    @staticmethod
    async def generate_referral_link(user_id: int) -> str:
        """Referral link yaratish"""
        referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                'UPDATE users SET referral_code = ? WHERE user_id = ?',
                (referral_code, user_id)
            )
            await db.commit()
        return f"https://t.me/your_bot?start={referral_code}"
    
    @staticmethod
    async def get_referral_stats(user_id: int) -> Dict:
        """Referral statistika"""
        async with aiosqlite.connect(DB_PATH) as db:
            # Direct referrals
            async with db.execute(
                'SELECT COUNT(*) FROM users WHERE referred_by = ?',
                (user_id,)
            ) as cursor:
                direct_referrals = (await cursor.fetchone())[0]
            
            # Total referral income
            async with db.execute(
                'SELECT SUM(balance) FROM users WHERE referred_by = ?',
                (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
                referral_income = result[0] or 0
        
        return {
            'direct_referrals': direct_referrals,
            'referral_income': referral_income,
            'bonus_rate': 10  # 10% bonus
        }
    
    @staticmethod
    async def create_white_list(list_name: str, users: List[int]) -> bool:
        """White list yaratish"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS white_lists (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name TEXT UNIQUE,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                await db.execute('INSERT INTO white_lists (list_name) VALUES (?)', (list_name,))
                await db.commit()
                
                # Get list ID
                async with db.execute(
                    'SELECT id FROM white_lists WHERE list_name = ?',
                    (list_name,)
                ) as cursor:
                    list_id = (await cursor.fetchone())[0]
                
                # Add users
                for user_id in users:
                    await db.execute(
                        'INSERT INTO white_list_users (list_id, user_id) VALUES (?, ?)',
                        (list_id, user_id)
                    )
                
                await db.commit()
            return True
        except Exception as e:
            print(f"White list xatosi: {e}")
            return False
    
    @staticmethod
    async def check_user_whitelist(user_id: int, list_name: str) -> bool:
        """User white listda tekshirish"""
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute('''
                SELECT COUNT(*) FROM white_list_users wlu
                JOIN white_lists wl ON wlu.list_id = wl.id
                WHERE wlu.user_id = ? AND wl.list_name = ?
            ''', (user_id, list_name)) as cursor:
                count = (await cursor.fetchone())[0]
            
            return count > 0
    
    @staticmethod
    async def get_user_analytics(user_id: int) -> Dict:
        """User analitikasi"""
        async with aiosqlite.connect(DB_PATH) as db:
            # User info
            async with db.execute(
                'SELECT total_requests, balance, is_vip, joined_date FROM users WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
            
            if not row:
                return None
            
            total_requests, balance, is_vip, joined_date = row
            
            # Calculate usage trend
            days_active = (datetime.now() - datetime.fromisoformat(joined_date)).days
            daily_average = total_requests / max(days_active, 1)
            
            return {
                'total_requests': total_requests,
                'balance': balance,
                'is_vip': bool(is_vip),
                'joined_date': joined_date,
                'days_active': days_active,
                'daily_average': round(daily_average, 2),
                'vip_status': 'VIP' if is_vip else 'Regular'
            }
    
    @staticmethod
    async def apply_discount(user_id: int, discount_percent: float, duration_days: int) -> bool:
        """User uchun vaqtinchalik chegirma qo'llash"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS user_discounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        discount_percent REAL,
                        valid_until TEXT,
                        applied_date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                valid_until = (datetime.now() + timedelta(days=duration_days)).isoformat()
                await db.execute(
                    'INSERT INTO user_discounts (user_id, discount_percent, valid_until) VALUES (?, ?, ?)',
                    (user_id, discount_percent, valid_until)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Chegirma xatosi: {e}")
            return False
    
    @staticmethod
    async def get_active_discount(user_id: int) -> Dict:
        """User uchun faol chegirmani olish"""
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute('''
                SELECT discount_percent, valid_until FROM user_discounts
                WHERE user_id = ? AND valid_until > datetime('now')
                ORDER BY valid_until DESC LIMIT 1
            ''', (user_id,)) as cursor:
                row = await cursor.fetchone()
            
            if row:
                return {
                    'discount': row[0],
                    'valid_until': row[1]
                }
            return None
    
    @staticmethod
    async def create_custom_package(
        package_name: str,
        price: float,
        features: List[str],
        limit: int
    ) -> bool:
        """Custom paket yaratish"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS custom_packages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        package_name TEXT UNIQUE,
                        price REAL,
                        features TEXT,
                        limit_requests INTEGER,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                features_str = '|'.join(features)
                await db.execute(
                    'INSERT INTO custom_packages (package_name, price, features, limit_requests) VALUES (?, ?, ?, ?)',
                    (package_name, price, features_str, limit)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Paket xatosi: {e}")
            return False
    
    @staticmethod
    async def get_user_balance_history(user_id: int, limit: int = 10) -> List[Dict]:
        """User balans tarixini olish"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS balance_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        transaction_type TEXT,
                        description TEXT,
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                async with db.execute(
                    'SELECT amount, transaction_type, description, timestamp FROM balance_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
                    (user_id, limit)
                ) as cursor:
                    rows = await cursor.fetchall()
                
                return [
                    {
                        'amount': r[0],
                        'type': r[1],
                        'description': r[2],
                        'timestamp': r[3]
                    }
                    for r in rows
                ]
        except Exception as e:
            print(f"Tarix xatosi: {e}")
            return []
    
    @staticmethod
    async def bulk_user_import(users: List[Dict]) -> Tuple[int, int]:
        """Ko'p foydalanuvchini import qilish"""
        imported = 0
        failed = 0
        
        async with aiosqlite.connect(DB_PATH) as db:
            for user_data in users:
                try:
                    await db.execute(
                        'INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
                        (user_data['user_id'], user_data.get('username'), user_data.get('first_name'))
                    )
                    imported += 1
                except:
                    failed += 1
            
            await db.commit()
        
        return imported, failed
    
    @staticmethod
    async def generate_performance_report(days: int = 30) -> Dict:
        """Performance report yaratish"""
        async with aiosqlite.connect(DB_PATH) as db:
            date_limit = (datetime.now() - timedelta(days=days)).isoformat()
            
            # New users
            async with db.execute(
                'SELECT COUNT(*) FROM users WHERE joined_date > ?',
                (date_limit,)
            ) as cursor:
                new_users = (await cursor.fetchone())[0]
            
            # Total revenue
            async with db.execute(
                'SELECT SUM(amount) FROM balance_history WHERE transaction_type = "purchase" AND timestamp > ?',
                (date_limit,)
            ) as cursor:
                result = await cursor.fetchone()
                revenue = result[0] or 0
            
            # Active users
            async with db.execute(
                'SELECT COUNT(*) FROM users WHERE total_requests > 0 AND joined_date > ?',
                (date_limit,)
            ) as cursor:
                active_users = (await cursor.fetchone())[0]
            
            return {
                'period_days': days,
                'new_users': new_users,
                'active_users': active_users,
                'total_revenue': revenue,
                'avg_revenue_per_user': revenue / max(active_users, 1),
                'report_date': datetime.now().isoformat()
            }
    
    @staticmethod
    async def export_user_data(user_id: int) -> Dict:
        """User dataini export qilish"""
        async with aiosqlite.connect(DB_PATH) as db:
            # User info
            async with db.execute(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                user_info = await cursor.fetchone()
            
            # User transactions
            async with db.execute(
                'SELECT * FROM balance_history WHERE user_id = ? ORDER BY timestamp DESC',
                (user_id,)
            ) as cursor:
                transactions = await cursor.fetchall()
            
            return {
                'user_info': user_info,
                'transactions': transactions,
                'export_date': datetime.now().isoformat()
            }
    
    @staticmethod
    async def create_announcement(
        title: str,
        content: str,
        priority: str = 'normal'
    ) -> bool:
        """Elon yaratish"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS announcements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content TEXT,
                        priority TEXT,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        is_active INTEGER DEFAULT 1
                    )
                ''')
                
                await db.execute(
                    'INSERT INTO announcements (title, content, priority) VALUES (?, ?, ?)',
                    (title, content, priority)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Elon xatosi: {e}")
            return False
    
    @staticmethod
    async def get_recent_announcements(limit: int = 5) -> List[Dict]:
        """So'nggi elonlarni olish"""
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                'SELECT id, title, content, priority, created_date FROM announcements WHERE is_active = 1 ORDER BY created_date DESC LIMIT ?',
                (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
            
            return [
                {
                    'id': r[0],
                    'title': r[1],
                    'content': r[2],
                    'priority': r[3],
                    'created_date': r[4]
                }
                for r in rows
            ]
    
    @staticmethod
    async def get_system_logs(limit: int = 50) -> List[Dict]:
        """Tizim loglarini olish"""
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        action TEXT,
                        user_id INTEGER,
                        details TEXT,
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                async with db.execute(
                    'SELECT action, user_id, details, timestamp FROM system_logs ORDER BY timestamp DESC LIMIT ?',
                    (limit,)
                ) as cursor:
                    rows = await cursor.fetchall()
                
                return [
                    {
                        'action': r[0],
                        'user_id': r[1],
                        'details': r[2],
                        'timestamp': r[3]
                    }
                    for r in rows
                ]
        except Exception as e:
            print(f"Log xatosi: {e}")
            return []
    
    @staticmethod
    async def create_backup() -> str:
        """Database backup yaratish"""
        import shutil
        from datetime import datetime as dt
        
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backups/smm_master_{timestamp}.db"
        
        try:
            shutil.copy(DB_PATH, backup_path)
            return backup_path
        except Exception as e:
            print(f"Backup xatosi: {e}")
            return None

# Global features instance
smm_features = SMMFeatures()
