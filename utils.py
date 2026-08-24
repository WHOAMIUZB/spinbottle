"""
Utility functions for SMM Master Bot
"""

import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict

# Setup logging
def setup_logging():
    """Setup logging configuration"""
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler('logs/smm_master.log')
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# Format functions
def format_currency(amount: float) -> str:
    """Format currency"""
    return f"${amount:,.2f}"

def format_datetime(dt: str) -> str:
    """Format datetime"""
    try:
        dt_obj = datetime.fromisoformat(dt)
        return dt_obj.strftime("%d.%m.%Y %H:%M")
    except:
        return dt

def format_number(num: int) -> str:
    """Format number with thousand separator"""
    return f"{num:,}"

# Validation functions
def is_valid_token(token: str) -> bool:
    """Check if token format is valid"""
    return ":" in token and len(token.split(":")[0]) > 5

def is_valid_user_id(user_id: int) -> bool:
    """Check if user ID is valid"""
    return isinstance(user_id, int) and user_id > 0

def is_valid_email(email: str) -> bool:
    """Check if email format is valid"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Text formatting
def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def bold(text: str) -> str:
    """Make text bold in HTML"""
    return f"<b>{text}</b>"

def italic(text: str) -> str:
    """Make text italic in HTML"""
    return f"<i>{text}</i>"

def code(text: str) -> str:
    """Format text as code in HTML"""
    return f"<code>{text}</code>"

# Statistics functions
def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0
    return (value / total) * 100

def calculate_growth(current: float, previous: float) -> float:
    """Calculate growth percentage"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def get_days_ago(date_str: str) -> int:
    """Get number of days ago from date string"""
    try:
        date = datetime.fromisoformat(date_str)
        return (datetime.now() - date).days
    except:
        return 0

# Message formatting
def create_stats_message(stats: Dict) -> str:
    """Create formatted statistics message"""
    message = "<b>📊 Statistika</b>\n\n"
    
    for key, value in stats.items():
        emoji = get_emoji_for_key(key)
        formatted_key = key.replace('_', ' ').title()
        message += f"{emoji} <b>{formatted_key}:</b> {format_number(value)}\n"
    
    return message

def get_emoji_for_key(key: str) -> str:
    """Get emoji for statistics key"""
    emojis = {
        'total_users': '👥',
        'total_messages': '📨',
        'active_bots': '🤖',
        'api_usage': '🔑',
        'revenue': '💰',
        'new_users': '🆕',
        'active_users': '🟢',
    }
    return emojis.get(key, '📊')

# Pagination
def paginate_list(items: List, page: int = 1, per_page: int = 5) -> Dict:
    """Paginate a list"""
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages
    }

# Time utilities
def get_time_period_label(days: int) -> str:
    """Get label for time period"""
    if days == 1:
        return "Bugun"
    elif days == 7:
        return "Shu hafta"
    elif days == 30:
        return "Shu oy"
    elif days == 365:
        return "Shu yil"
    else:
        return f"Oxirgi {days} kun"

def get_next_date(days_ahead: int) -> str:
    """Get date string for days ahead"""
    date = datetime.now() + timedelta(days=days_ahead)
    return date.isoformat()

# File utilities
def ensure_directory_exists(directory: str):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)

def get_file_size(file_path: str) -> str:
    """Get human readable file size"""
    size = os.path.getsize(file_path)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    
    return f"{size:.2f} TB"

# Data formatting
def format_api_info(api: Dict) -> str:
    """Format API information"""
    return (
        f"<b>{api['api_name']}</b>\n"
        f"💰 Narxi: {format_currency(api['price'])}\n"
        f"📊 Ishlatilgan: {format_number(api['used_requests'])}/{format_number(api['limit_requests'])}\n"
        f"📂 Kategoriya: {api['category']}"
    )

def format_user_info(user: Dict) -> str:
    """Format user information"""
    return (
        f"👤 <b>{user.get('username', 'N/A')}</b>\n"
        f"📝 Ismi: {user.get('first_name', 'N/A')}\n"
        f"🆔 ID: <code>{user.get('user_id', 'N/A')}</code>\n"
        f"💰 Balans: {format_currency(user.get('balance', 0))}\n"
        f"📊 Jami so'rovlar: {format_number(user.get('total_requests', 0))}"
    )

# Init utilities
def initialize_directories():
    """Initialize required directories"""
    ensure_directory_exists('logs')
    ensure_directory_exists('backups')
    ensure_directory_exists('data')

# Version info
VERSION = "1.0.0"
AUTHOR = "Zoirbek"
CREATED_DATE = "2024-01-15"

def get_version_info() -> str:
    """Get version information"""
    return f"""
🤖 SMM Master Bot v{VERSION}
👤 Created by: {AUTHOR}
📅 Created: {CREATED_DATE}
✨ 30+ Features
🚀 Active Development
    """

# Status codes
STATUS_CODES = {
    'success': 200,
    'created': 201,
    'bad_request': 400,
    'unauthorized': 401,
    'forbidden': 403,
    'not_found': 404,
    'server_error': 500
}

def get_status_message(code: int) -> str:
    """Get status message"""
    messages = {
        200: "✅ Muvaffaqiyatli",
        201: "✅ Yaratildi",
        400: "❌ Noto'g'ri so'rov",
        401: "❌ Avtentifikatsiya kerak",
        403: "❌ Ruxsat yo'q",
        404: "❌ Topilmadi",
        500: "❌ Server xatosi"
    }
    return messages.get(code, "❌ Noma'lum xato")
