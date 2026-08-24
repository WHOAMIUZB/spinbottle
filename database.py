import aiosqlite
import os
from datetime import datetime
from typing import List, Dict, Tuple

DB_PATH = "smm_master.db"

async def init_db():
    """Initialize database with all required tables"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Bot tokens table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS bot_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE NOT NULL,
                bot_name TEXT NOT NULL,
                bot_id INTEGER,
                added_date TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                user_count INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0
            )
        ''')
        
        # API keys table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                price REAL DEFAULT 0,
                limit_requests INTEGER DEFAULT 1000,
                used_requests INTEGER DEFAULT 0,
                added_date TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                category TEXT
            )
        ''')
        
        # Users table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_date TEXT DEFAULT CURRENT_TIMESTAMP,
                total_requests INTEGER DEFAULT 0,
                balance REAL DEFAULT 0,
                referral_code TEXT UNIQUE,
                referred_by INTEGER,
                is_banned INTEGER DEFAULT 0,
                is_vip INTEGER DEFAULT 0
            )
        ''')
        
        # Broadcast logs
        await db.execute('''
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                broadcast_date TEXT DEFAULT CURRENT_TIMESTAMP,
                bot_token TEXT,
                message_type TEXT,
                content TEXT,
                sent_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                total_users INTEGER DEFAULT 0
            )
        ''')
        
        # Promo codes
        await db.execute('''
            CREATE TABLE IF NOT EXISTS promo_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                discount_percent REAL,
                max_uses INTEGER,
                used_count INTEGER DEFAULT 0,
                valid_until TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Settings
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT
            )
        ''')
        
        # Statistics
        await db.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_date TEXT DEFAULT CURRENT_TIMESTAMP,
                total_users INTEGER,
                total_messages INTEGER,
                api_usage INTEGER,
                revenue REAL,
                active_bots INTEGER
            )
        ''')
        
        # Scheduled messages
        await db.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_time TEXT NOT NULL,
                message_text TEXT,
                message_type TEXT,
                bot_tokens TEXT,
                is_sent INTEGER DEFAULT 0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await db.commit()

# Bot Token Functions
async def add_bot_token(token: str, bot_name: str) -> bool:
    """Add new bot token"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                'INSERT INTO bot_tokens (token, bot_name) VALUES (?, ?)',
                (token, bot_name)
            )
            await db.commit()
        return True
    except:
        return False

async def get_all_bot_tokens() -> List[Dict]:
    """Get all active bot tokens"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT token, bot_name, bot_id, user_count, message_count FROM bot_tokens WHERE is_active = 1'
        ) as cursor:
            rows = await cursor.fetchall()
        return [
            {'token': r[0], 'bot_name': r[1], 'bot_id': r[2], 'user_count': r[3], 'message_count': r[4]}
            for r in rows
        ]

async def remove_bot_token(token: str) -> bool:
    """Remove bot token"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE bot_tokens SET is_active = 0 WHERE token = ?', (token,))
        await db.commit()
    return True

# API Key Functions
async def add_api_key(api_name: str, api_key: str, price: float, category: str) -> bool:
    """Add new API key"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                'INSERT INTO api_keys (api_name, api_key, price, category) VALUES (?, ?, ?, ?)',
                (api_name, api_key, price, category)
            )
            await db.commit()
        return True
    except:
        return False

async def get_all_apis() -> List[Dict]:
    """Get all active APIs"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT id, api_name, api_key, price, used_requests, limit_requests, category FROM api_keys WHERE is_active = 1'
        ) as cursor:
            rows = await cursor.fetchall()
        return [
            {
                'id': r[0], 'api_name': r[1], 'api_key': r[2], 'price': r[3],
                'used_requests': r[4], 'limit_requests': r[5], 'category': r[6]
            }
            for r in rows
        ]

async def update_api_price(api_id: int, new_price: float) -> bool:
    """Update API price"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE api_keys SET price = ? WHERE id = ?', (new_price, api_id))
        await db.commit()
    return True

async def remove_api(api_id: int) -> bool:
    """Remove API"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE api_keys SET is_active = 0 WHERE id = ?', (api_id,))
        await db.commit()
    return True

# User Functions
async def add_user(user_id: int, username: str = None, first_name: str = None) -> bool:
    """Add new user"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                'INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
                (user_id, username, first_name)
            )
            await db.commit()
        return True
    except:
        return False

async def get_user_stats(user_id: int) -> Dict:
    """Get user statistics"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT total_requests, balance, is_vip, referral_code FROM users WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
        if row:
            return {
                'total_requests': row[0],
                'balance': row[1],
                'is_vip': row[2],
                'referral_code': row[3]
            }
    return None

async def ban_user(user_id: int) -> bool:
    """Ban user"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
        await db.commit()
    return True

async def unban_user(user_id: int) -> bool:
    """Unban user"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
        await db.commit()
    return True

# Promo Code Functions
async def create_promo_code(code: str, discount: float, max_uses: int, valid_until: str) -> bool:
    """Create promo code"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                'INSERT INTO promo_codes (code, discount_percent, max_uses, valid_until) VALUES (?, ?, ?, ?)',
                (code, discount, max_uses, valid_until)
            )
            await db.commit()
        return True
    except:
        return False

async def apply_promo_code(code: str, user_id: int) -> Dict:
    """Apply promo code to user"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT discount_percent, max_uses, used_count FROM promo_codes WHERE code = ? AND is_active = 1',
            (code,)
        ) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return {'success': False, 'message': 'Promo kod topilmadi'}
        
        discount, max_uses, used_count = row
        if used_count >= max_uses:
            return {'success': False, 'message': 'Promo kod cheklangani tugadi'}
        
        await db.execute(
            'UPDATE promo_codes SET used_count = used_count + 1 WHERE code = ?',
            (code,)
        )
        await db.commit()
        return {'success': True, 'discount': discount}

# Statistics Functions
async def log_broadcast(bot_token: str, message_type: str, content: str, sent_count: int):
    """Log broadcast message"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT INTO broadcasts (bot_token, message_type, content, sent_count) VALUES (?, ?, ?, ?)',
            (bot_token, message_type, content, sent_count)
        )
        await db.commit()

async def get_statistics() -> Dict:
    """Get overall statistics"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Total users
        async with db.execute('SELECT COUNT(*) FROM users WHERE is_banned = 0') as cursor:
            total_users = (await cursor.fetchone())[0]
        
        # Total messages
        async with db.execute('SELECT SUM(message_count) FROM bot_tokens') as cursor:
            result = await cursor.fetchone()
            total_messages = result[0] or 0
        
        # Active bots
        async with db.execute('SELECT COUNT(*) FROM bot_tokens WHERE is_active = 1') as cursor:
            active_bots = (await cursor.fetchone())[0]
        
        # API usage
        async with db.execute('SELECT SUM(used_requests) FROM api_keys') as cursor:
            result = await cursor.fetchone()
            api_usage = result[0] or 0
        
        return {
            'total_users': total_users,
            'total_messages': total_messages,
            'active_bots': active_bots,
            'api_usage': api_usage
        }

async def get_detailed_stats() -> List[Dict]:
    """Get detailed statistics for all bots"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            'SELECT bot_name, user_count, message_count, added_date FROM bot_tokens WHERE is_active = 1'
        ) as cursor:
            rows = await cursor.fetchall()
        return [
            {
                'bot_name': r[0],
                'user_count': r[1],
                'message_count': r[2],
                'added_date': r[3]
            }
            for r in rows
        ]
