"""
Spin the Bottle - Ma'lumotlar bazasi qatlami (aiosqlite asosida)
Barcha jadvallar, boshlang'ich (seed) ma'lumotlar va yordamchi funksiyalar shu yerda.
"""
import json
import random
import time
from typing import Any, Optional

import aiosqlite

from config import DB_PATH, ADMIN_ID

# ---------------------------------------------------------------------------
# SXEMA
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY,           -- telegram user id
    username        TEXT,
    first_name      TEXT,
    photo_url       TEXT,
    hearts          INTEGER NOT NULL DEFAULT 100,
    spins           INTEGER NOT NULL DEFAULT 3,     -- g'ildirakni bepul aylantirish soni (Шансы)
    is_vip          INTEGER NOT NULL DEFAULT 0,
    is_banned       INTEGER NOT NULL DEFAULT 0,
    is_admin        INTEGER NOT NULL DEFAULT 0,
    referred_by     INTEGER,
    claimed_free    INTEGER NOT NULL DEFAULT 0,     -- bepul hearts (invite/subscribe) olinganmi
    room_id         INTEGER,
    seat_index      INTEGER,
    created_at      INTEGER NOT NULL,
    last_seen       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji           TEXT NOT NULL,
    name            TEXT NOT NULL,
    cost            INTEGER NOT NULL DEFAULT 1,     -- yuboruvchidan yechiladigan hearts
    points          INTEGER NOT NULL DEFAULT 1,     -- qabul qiluvchiga qo'shiladigan ball/hearts
    is_active       INTEGER NOT NULL DEFAULT 1,
    sort_order      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS wheel_prizes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    label           TEXT NOT NULL,                  -- masalan "100" yoki "Jackpot"
    hearts_reward   INTEGER NOT NULL,
    weight          INTEGER NOT NULL DEFAULT 10,     -- ehtimollik og'irligi (katta = ko'p tushadi)
    color           TEXT NOT NULL DEFAULT '#2ecc71',
    icon            TEXT NOT NULL DEFAULT '❤️',
    is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS shop_packages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    hearts_amount   INTEGER NOT NULL,
    stars_price     INTEGER NOT NULL,
    bonus_percent   INTEGER NOT NULL DEFAULT 0,
    badge           TEXT,                            -- masalan "Выгодно" / "Хит" / null
    sort_order      INTEGER NOT NULL DEFAULT 0,
    is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rooms (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    seats           INTEGER NOT NULL DEFAULT 8,
    is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id         INTEGER NOT NULL,
    user_id         INTEGER,
    text            TEXT,
    reaction_id     INTEGER,
    created_at      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    type            TEXT NOT NULL,                   -- spin_bottle, wheel, reaction_sent, reaction_recv, shop, free, admin_adjust
    amount          INTEGER NOT NULL,
    description     TEXT,
    created_at      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key             TEXT PRIMARY KEY,
    value           TEXT
);
"""

DEFAULT_SETTINGS = {
    "required_channel": "@spinthe_channel",
    "referral_bonus": "20",
    "subscribe_bonus": "5",
    "compliment_bonus": "10",
    "wheel_spin_cost": "1",
    "game_title": "Spin the Bottle 🍾❤️",
    "sound_enabled": "1",
    "music_enabled": "1",
}

DEFAULT_REACTIONS = [
    # emoji, name, cost(yuboruvchidan), points(qabul qiluvchiga), sort
    ("🎉", "Xursandchilik", 2, 2, 1),
    ("🎂", "Tort", 1, 1, 2),
    ("👑", "Toj (kichik)", 3, 3, 3),
    ("👑", "Toj (o'rta)", 3, 3, 4),
    ("👑", "Toj (katta)", 3, 3, 5),
    ("🌀", "Ventilyator", 1, 1, 6),
    ("⚽", "Futbol to'pi", 1, 1, 7),
    ("🔧", "Kalit", 1, 1, 8),
    ("🍢", "Kabob", 1, 1, 9),
    ("💋", "O'pish", 1, 1, 10),
    ("💎", "Olmos", 1, 1, 11),
    ("🍓", "Qulupnay", 1, 1, 12),
    ("🍅", "Pomidor", 1, 1, 13),
    ("🐸", "Qurbaqa", 2, 2, 14),
    ("🌹", "Atirgul", 1, 1, 15),
]

DEFAULT_WHEEL_PRIZES = [
    ("3", 3, 20, "#2ecc71", "❤️"),
    ("7", 7, 15, "#27ae60", "❤️"),
    ("25", 25, 8, "#16a085", "❤️"),
    ("1", 1, 25, "#2ecc71", "❤️"),
    ("100", 100, 3, "#f39c12", "⭐"),
    ("5", 5, 15, "#2ecc71", "❤️"),
    ("3", 3, 20, "#27ae60", "❤️"),
    ("1000", 1000, 1, "#e74c3c", "🏆"),
    ("1", 1, 25, "#16a085", "❤️"),
    ("3", 3, 20, "#2ecc71", "❤️"),
]

DEFAULT_SHOP_PACKAGES = [
    (7000, 5000, 40, "Выгодно", 1),
    (3125, 2500, 25, None, 2),
    (1200, 1000, 20, "Хит", 3),
    (500, 500, 0, None, 4),
    (250, 250, 0, None, 5),
    (50, 50, 0, None, 6),
]


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys = ON")
    return db


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.executescript(SCHEMA)

        # settings
        for k, v in DEFAULT_SETTINGS.items():
            await db.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v)
            )

        # reactions (faqat bo'sh bo'lsa seed qilamiz)
        cur = await db.execute("SELECT COUNT(*) c FROM reactions")
        if (await cur.fetchone())["c"] == 0:
            await db.executemany(
                "INSERT INTO reactions (emoji, name, cost, points, sort_order) VALUES (?,?,?,?,?)",
                DEFAULT_REACTIONS,
            )

        cur = await db.execute("SELECT COUNT(*) c FROM wheel_prizes")
        if (await cur.fetchone())["c"] == 0:
            await db.executemany(
                "INSERT INTO wheel_prizes (label, hearts_reward, weight, color, icon) VALUES (?,?,?,?,?)",
                DEFAULT_WHEEL_PRIZES,
            )

        cur = await db.execute("SELECT COUNT(*) c FROM shop_packages")
        if (await cur.fetchone())["c"] == 0:
            await db.executemany(
                "INSERT INTO shop_packages (hearts_amount, stars_price, bonus_percent, badge, sort_order) VALUES (?,?,?,?,?)",
                DEFAULT_SHOP_PACKAGES,
            )

        cur = await db.execute("SELECT COUNT(*) c FROM rooms")
        if (await cur.fetchone())["c"] == 0:
            await db.execute(
                "INSERT INTO rooms (name, seats) VALUES (?, ?)", ("Стол 204", 8)
            )

        await db.commit()


# ---------------------------------------------------------------------------
# FOYDALANUVCHILAR
# ---------------------------------------------------------------------------

async def get_or_create_user(user_id: int, username: str = None, first_name: str = None,
                              photo_url: str = None, referred_by: int = None) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = await cur.fetchone()
        now = int(time.time())
        if row:
            await db.execute(
                "UPDATE users SET username=?, first_name=?, photo_url=?, last_seen=? WHERE id=?",
                (username, first_name, photo_url, now, user_id),
            )
            await db.commit()
            cur = await db.execute("SELECT * FROM users WHERE id=?", (user_id,))
            row = await cur.fetchone()
            return dict(row)
        else:
            is_admin = 1 if user_id == ADMIN_ID else 0
            # room_id/seat_index ataylab bo'sh qoldiriladi - keyinroq seat_user() orqali to'g'ri joy beriladi
            await db.execute(
                """INSERT INTO users (id, username, first_name, photo_url, hearts, spins,
                   is_admin, referred_by, created_at, last_seen)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (user_id, username, first_name, photo_url, 100, 3, is_admin,
                 referred_by, now, now),
            )
            if referred_by and referred_by != user_id:
                bonus = int(await get_setting("referral_bonus") or 20)
                await db.execute(
                    "UPDATE users SET hearts = hearts + ? WHERE id=?", (bonus, referred_by)
                )
                await db.execute(
                    "INSERT INTO transactions (user_id, type, amount, description, created_at) VALUES (?,?,?,?,?)",
                    (referred_by, "referral", bonus, f"Referal: {user_id} qo'shildi", now),
                )
            await db.commit()
            cur = await db.execute("SELECT * FROM users WHERE id=?", (user_id,))
            row = await cur.fetchone()
            return dict(row)


async def get_user(user_id: int) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def add_hearts(user_id: int, amount: int, tx_type: str, description: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET hearts = MAX(0, hearts + ?) WHERE id=?", (amount, user_id))
        await db.execute(
            "INSERT INTO transactions (user_id, type, amount, description, created_at) VALUES (?,?,?,?,?)",
            (user_id, tx_type, amount, description, int(time.time())),
        )
        await db.commit()


async def list_users(limit=200, offset=0, search: str = None) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if search:
            cur = await db.execute(
                "SELECT * FROM users WHERE username LIKE ? OR first_name LIKE ? OR CAST(id AS TEXT) LIKE ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (f"%{search}%", f"%{search}%", f"%{search}%", limit, offset),
            )
        else:
            cur = await db.execute(
                "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset)
            )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def set_user_field(user_id: int, field: str, value: Any):
    allowed = {"hearts", "spins", "is_vip", "is_banned", "is_admin", "room_id", "seat_index"}
    if field not in allowed:
        raise ValueError("Field ruxsat etilmagan")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE users SET {field}=? WHERE id=?", (value, user_id))
        await db.commit()


# ---------------------------------------------------------------------------
# REAKSIYALAR (ADMIN BOSHQARADI)
# ---------------------------------------------------------------------------

async def list_reactions(only_active=True) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        q = "SELECT * FROM reactions"
        if only_active:
            q += " WHERE is_active=1"
        q += " ORDER BY sort_order ASC, id ASC"
        cur = await db.execute(q)
        return [dict(r) for r in await cur.fetchall()]


async def create_reaction(emoji, name, cost, points, sort_order=0) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO reactions (emoji, name, cost, points, sort_order) VALUES (?,?,?,?,?)",
            (emoji, name, cost, points, sort_order),
        )
        await db.commit()
        return cur.lastrowid


async def update_reaction(rid: int, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k}=?" for k in fields)
    vals = list(fields.values()) + [rid]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE reactions SET {cols} WHERE id=?", vals)
        await db.commit()


async def delete_reaction(rid: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM reactions WHERE id=?", (rid,))
        await db.commit()


async def get_reaction(rid: int) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM reactions WHERE id=?", (rid,))
        row = await cur.fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------------
# BAXT G'ILDIRAGI SOVG'ALARI (ADMIN BOSHQARADI)
# ---------------------------------------------------------------------------

async def list_wheel_prizes(only_active=True) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        q = "SELECT * FROM wheel_prizes"
        if only_active:
            q += " WHERE is_active=1"
        q += " ORDER BY id ASC"
        cur = await db.execute(q)
        return [dict(r) for r in await cur.fetchall()]


async def create_wheel_prize(label, hearts_reward, weight, color, icon) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO wheel_prizes (label, hearts_reward, weight, color, icon) VALUES (?,?,?,?,?)",
            (label, hearts_reward, weight, color, icon),
        )
        await db.commit()
        return cur.lastrowid


async def update_wheel_prize(pid: int, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k}=?" for k in fields)
    vals = list(fields.values()) + [pid]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE wheel_prizes SET {cols} WHERE id=?", vals)
        await db.commit()


async def delete_wheel_prize(pid: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM wheel_prizes WHERE id=?", (pid,))
        await db.commit()


async def pick_random_prize() -> Optional[dict]:
    prizes = await list_wheel_prizes(only_active=True)
    if not prizes:
        return None
    weights = [p["weight"] for p in prizes]
    return random.choices(prizes, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# DO'KON PAKETLARI (ADMIN BOSHQARADI)
# ---------------------------------------------------------------------------

async def list_shop_packages(only_active=True) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        q = "SELECT * FROM shop_packages"
        if only_active:
            q += " WHERE is_active=1"
        q += " ORDER BY sort_order ASC"
        cur = await db.execute(q)
        return [dict(r) for r in await cur.fetchall()]


async def create_shop_package(hearts_amount, stars_price, bonus_percent, badge, sort_order) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO shop_packages (hearts_amount, stars_price, bonus_percent, badge, sort_order) VALUES (?,?,?,?,?)",
            (hearts_amount, stars_price, bonus_percent, badge, sort_order),
        )
        await db.commit()
        return cur.lastrowid


async def update_shop_package(pid: int, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k}=?" for k in fields)
    vals = list(fields.values()) + [pid]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE shop_packages SET {cols} WHERE id=?", vals)
        await db.commit()


async def delete_shop_package(pid: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM shop_packages WHERE id=?", (pid,))
        await db.commit()


# ---------------------------------------------------------------------------
# XONALAR / STOLLAR
# ---------------------------------------------------------------------------

async def get_room_with_users(room_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM rooms WHERE id=?", (room_id,))
        room = await cur.fetchone()
        cur = await db.execute(
            "SELECT id, username, first_name, photo_url, seat_index, is_vip FROM users WHERE room_id=? ORDER BY seat_index",
            (room_id,),
        )
        users = [dict(r) for r in await cur.fetchall()]
        return {"room": dict(room) if room else None, "users": users}


async def list_rooms() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM rooms ORDER BY id")
        return [dict(r) for r in await cur.fetchall()]


async def create_room(name: str, seats: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("INSERT INTO rooms (name, seats) VALUES (?,?)", (name, seats))
        await db.commit()
        return cur.lastrowid


async def seat_user(user_id: int, room_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT seats FROM rooms WHERE id=?", (room_id,))
        room = await cur.fetchone()
        if not room:
            raise ValueError("Xona topilmadi")
        cur = await db.execute("SELECT seat_index FROM users WHERE room_id=?", (room_id,))
        taken = {r["seat_index"] for r in await cur.fetchall() if r["seat_index"] is not None}
        seat = None
        for i in range(room["seats"]):
            if i not in taken:
                seat = i
                break
        if seat is None:
            seat = 0
        await db.execute("UPDATE users SET room_id=?, seat_index=? WHERE id=?", (room_id, seat, user_id))
        await db.commit()
        return seat


# ---------------------------------------------------------------------------
# CHAT
# ---------------------------------------------------------------------------

async def add_chat_message(room_id: int, user_id: int = None, text: str = None, reaction_id: int = None) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        now = int(time.time())
        cur = await db.execute(
            "INSERT INTO chat_messages (room_id, user_id, text, reaction_id, created_at) VALUES (?,?,?,?,?)",
            (room_id, user_id, text, reaction_id, now),
        )
        await db.commit()
        return {"id": cur.lastrowid, "room_id": room_id, "user_id": user_id, "text": text,
                "reaction_id": reaction_id, "created_at": now}


async def list_chat_messages(room_id: int, limit=50) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM chat_messages WHERE room_id=? ORDER BY id DESC LIMIT ?", (room_id, limit)
        )
        rows = [dict(r) for r in await cur.fetchall()]
        rows.reverse()
        return rows


# ---------------------------------------------------------------------------
# SOZLAMALAR
# ---------------------------------------------------------------------------

async def get_setting(key: str) -> Optional[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = await cur.fetchone()
        return row["value"] if row else None


async def get_all_settings() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT key, value FROM settings")
        rows = await cur.fetchall()
        return {r["key"]: r["value"] for r in rows}


async def set_setting(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        await db.commit()


# ---------------------------------------------------------------------------
# STATISTIKA
# ---------------------------------------------------------------------------

async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        total_users = (await (await db.execute("SELECT COUNT(*) c FROM users")).fetchone())["c"]
        total_hearts = (await (await db.execute("SELECT COALESCE(SUM(hearts),0) s FROM users")).fetchone())["s"]
        total_vip = (await (await db.execute("SELECT COUNT(*) c FROM users WHERE is_vip=1")).fetchone())["c"]
        today_start = int(time.time()) - 86400
        new_today = (await (await db.execute(
            "SELECT COUNT(*) c FROM users WHERE created_at>=?", (today_start,))).fetchone())["c"]
        spins_today = (await (await db.execute(
            "SELECT COUNT(*) c FROM transactions WHERE type='wheel' AND created_at>=?", (today_start,))).fetchone())["c"]
        reactions_sent = (await (await db.execute(
            "SELECT COUNT(*) c FROM transactions WHERE type='reaction_sent'")).fetchone())["c"]
        shop_revenue_stars = (await (await db.execute(
            "SELECT COALESCE(SUM(ABS(amount)),0) s FROM transactions WHERE type='shop'")).fetchone())["s"]
        return {
            "total_users": total_users,
            "total_hearts_in_economy": total_hearts,
            "total_vip": total_vip,
            "new_users_today": new_today,
            "wheel_spins_today": spins_today,
            "reactions_sent_total": reactions_sent,
        }


async def list_transactions(limit=100) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in await cur.fetchall()]
