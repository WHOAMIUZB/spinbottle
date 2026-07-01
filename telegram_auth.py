"""
Telegram Mini App initData ni xavfsiz tekshirish (HMAC-SHA256).
https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""
import hashlib
import hmac
import json
import urllib.parse
from typing import Optional

from config import BOT_TOKEN


def validate_init_data(init_data: str) -> Optional[dict]:
    """initData satrini tekshiradi va foydalanuvchi ma'lumotini qaytaradi.
    Muvaffaqiyatsiz bo'lsa None qaytaradi."""
    if not init_data:
        return None
    try:
        parsed = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))
        received_hash = parsed.pop("hash", None)
        if not received_hash:
            return None

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(computed_hash, received_hash):
            return None

        user_json = parsed.get("user")
        user = json.loads(user_json) if user_json else None
        return {"user": user, "raw": parsed}
    except Exception:
        return None


def dev_fallback_user(user_id: int, first_name: str = "Test") -> dict:
    """Faqat lokal test uchun: initData bo'lmaganda soxta foydalanuvchi (DEV rejimda)."""
    return {"id": user_id, "first_name": first_name, "username": f"user{user_id}"}
