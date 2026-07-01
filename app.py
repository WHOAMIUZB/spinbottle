"""
Spin the Bottle - FastAPI backend
Mini App (o'yin) uchun API + to'liq Admin panel API + real-vaqt WebSocket.
Ishga tushirish: uvicorn app:app --host 0.0.0.0 --port 8000
"""
import asyncio
import json
import random
import time
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Header, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database as db
from config import ADMIN_ID, ADMIN_PANEL_SECRET, PORT
from telegram_auth import validate_init_data, dev_fallback_user

app = FastAPI(title="Spin the Bottle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await db.init_db()


# =============================================================================
# WEBSOCKET - REAL VAQT XONA YANGILANISHLARI
# =============================================================================

class RoomHub:
    def __init__(self):
        self.rooms: dict[int, set[WebSocket]] = {}

    async def connect(self, room_id: int, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room_id, set()).add(ws)

    def disconnect(self, room_id: int, ws: WebSocket):
        if room_id in self.rooms and ws in self.rooms[room_id]:
            self.rooms[room_id].discard(ws)

    async def broadcast(self, room_id: int, message: dict):
        dead = []
        for ws in self.rooms.get(room_id, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for d in dead:
            self.disconnect(room_id, d)


hub = RoomHub()


@app.websocket("/ws/room/{room_id}")
async def ws_room(websocket: WebSocket, room_id: int):
    await hub.connect(room_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # ping/keepalive
    except WebSocketDisconnect:
        hub.disconnect(room_id, websocket)


# =============================================================================
# AUTENTIFIKATSIYA YORDAMCHILARI
# =============================================================================

async def get_current_user(request: Request, x_init_data: Optional[str] = Header(None),
                            dev_user_id: Optional[int] = Query(None)) -> dict:
    """Telegram initData orqali foydalanuvchini aniqlaydi.
    DEV rejimda (brauzerda test qilish uchun) dev_user_id query param bilan ham ishlaydi."""
    init_data = x_init_data or request.headers.get("X-Init-Data")
    if init_data:
        result = validate_init_data(init_data)
        if not result or not result.get("user"):
            raise HTTPException(status_code=401, detail="initData yaroqsiz")
        tg_user = result["user"]
    elif dev_user_id:
        tg_user = dev_fallback_user(dev_user_id)
    else:
        raise HTTPException(status_code=401, detail="Autentifikatsiya talab qilinadi")

    user = await db.get_or_create_user(
        tg_user["id"],
        username=tg_user.get("username"),
        first_name=tg_user.get("first_name"),
        photo_url=tg_user.get("photo_url"),
    )
    if user["is_banned"]:
        raise HTTPException(status_code=403, detail="Siz bloklangansiz")
    if not user.get("room_id") or user.get("seat_index") is None:
        rooms = await db.list_rooms()
        if rooms:
            await db.seat_user(user["id"], user.get("room_id") or rooms[0]["id"])
            user = await db.get_user(user["id"])
    return user


async def require_admin(request: Request, x_init_data: Optional[str] = Header(None),
                         x_admin_secret: Optional[str] = Header(None),
                         dev_user_id: Optional[int] = Query(None)) -> dict:
    """Admin panel uchun avtorizatsiya: Telegram orqali (admin ID) yoki web parol orqali."""
    if x_admin_secret and x_admin_secret == ADMIN_PANEL_SECRET:
        return {"id": ADMIN_ID, "via": "secret"}

    init_data = x_init_data or request.headers.get("X-Init-Data")
    if init_data:
        result = validate_init_data(init_data)
        if result and result.get("user") and result["user"]["id"] == ADMIN_ID:
            return {"id": ADMIN_ID, "via": "telegram"}

    if dev_user_id and dev_user_id == ADMIN_ID:
        return {"id": ADMIN_ID, "via": "dev"}

    raise HTTPException(status_code=403, detail="Faqat admin uchun ruxsat etilgan")


# =============================================================================
# O'YIN API (FOYDALANUVCHI TOMONI)
# =============================================================================

@app.get("/api/me")
async def api_me(request: Request, x_init_data: Optional[str] = Header(None),
                  dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    return user


@app.get("/api/room")
async def api_room(request: Request, x_init_data: Optional[str] = Header(None),
                    dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    data = await db.get_room_with_users(user["room_id"])
    data["me"] = user
    return data


@app.get("/api/reactions")
async def api_reactions():
    return await db.list_reactions()


@app.get("/api/wheel-prizes")
async def api_wheel_prizes():
    return await db.list_wheel_prizes()


@app.get("/api/shop-packages")
async def api_shop_packages():
    return await db.list_shop_packages()


@app.get("/api/settings")
async def api_settings():
    s = await db.get_all_settings()
    # Faqat frontendga kerakli, xavfsiz sozlamalarni chiqaramiz
    public_keys = ["required_channel", "referral_bonus", "subscribe_bonus",
                   "compliment_bonus", "wheel_spin_cost", "game_title",
                   "sound_enabled", "music_enabled"]
    return {k: s.get(k) for k in public_keys}


@app.get("/api/chat")
async def api_chat(request: Request, x_init_data: Optional[str] = Header(None),
                    dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    return await db.list_chat_messages(user["room_id"])


class ChatIn(BaseModel):
    text: str


@app.post("/api/chat")
async def api_chat_send(body: ChatIn, request: Request, x_init_data: Optional[str] = Header(None),
                         dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    msg = await db.add_chat_message(user["room_id"], user_id=user["id"], text=body.text[:500])
    msg["first_name"] = user["first_name"]
    await hub.broadcast(user["room_id"], {"event": "chat", "data": msg})
    return msg


@app.post("/api/spin-bottle")
async def api_spin_bottle(request: Request, x_init_data: Optional[str] = Header(None),
                           dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    room_data = await db.get_room_with_users(user["room_id"])
    users = room_data["users"]
    if len(users) < 2:
        raise HTTPException(status_code=400, detail="Aylantirish uchun xonada kamida 2 kishi kerak")
    picked = random.sample(users, 2)
    outcomes = ["Поцелуются 💋", "Rad etdi 🙅", "Objatiya 🤗", "Hech narsa bo'lmadi 🙈"]
    result = {
        "pair": picked,
        "outcome": random.choice(outcomes),
    }
    await hub.broadcast(user["room_id"], {"event": "spin_bottle", "data": result})
    return result


class ReactionSendIn(BaseModel):
    reaction_id: int
    target_user_id: int


@app.post("/api/send-reaction")
async def api_send_reaction(body: ReactionSendIn, request: Request,
                             x_init_data: Optional[str] = Header(None),
                             dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    reaction = await db.get_reaction(body.reaction_id)
    if not reaction or not reaction["is_active"]:
        raise HTTPException(status_code=404, detail="Reaksiya topilmadi")
    if user["hearts"] < reaction["cost"]:
        raise HTTPException(status_code=400, detail="Hearts yetarli emas")
    target = await db.get_user(body.target_user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Qabul qiluvchi topilmadi")

    await db.add_hearts(user["id"], -reaction["cost"], "reaction_sent",
                         f"{reaction['emoji']} {reaction['name']} -> {target['id']}")
    await db.add_hearts(target["id"], reaction["points"], "reaction_recv",
                         f"{reaction['emoji']} {reaction['name']} <- {user['id']}")

    msg = await db.add_chat_message(user["room_id"], user_id=user["id"],
                                     text=f"{reaction['emoji']} {target.get('first_name','')} ga yubordi",
                                     reaction_id=reaction["id"])
    await hub.broadcast(user["room_id"], {"event": "reaction", "data": {
        "from": user["id"], "to": target["id"], "reaction": reaction, "message": msg
    }})
    return {"ok": True, "new_balance": user["hearts"] - reaction["cost"]}


@app.post("/api/spin-wheel")
async def api_spin_wheel(request: Request, x_init_data: Optional[str] = Header(None),
                          dev_user_id: Optional[int] = Query(None)):
    user = await get_current_user(request, x_init_data, dev_user_id)
    cost = int(await db.get_setting("wheel_spin_cost") or 1)

    if user["spins"] > 0:
        await db.set_user_field(user["id"], "spins", user["spins"] - 1)
    else:
        if user["hearts"] < cost * 20:  # aylantirish uchun hearts evaziga (masalan 1 chance = 20 hearts)
            raise HTTPException(status_code=400, detail="Aylantirish uchun 'Шансы' yoki yetarli hearts kerak")
        await db.add_hearts(user["id"], -(cost * 20), "wheel_buy_chance", "G'ildirak uchun chance sotib olindi")

    prize = await db.pick_random_prize()
    if not prize:
        raise HTTPException(status_code=500, detail="G'ildirak sovg'alari sozlanmagan")

    await db.add_hearts(user["id"], prize["hearts_reward"], "wheel", f"G'ildirakdan yutdi: {prize['label']}")
    await hub.broadcast(user["room_id"], {"event": "wheel_win", "data": {
        "user_id": user["id"], "first_name": user["first_name"], "prize": prize
    }})
    return {"prize": prize}


@app.post("/api/claim-free-hearts")
async def api_claim_free(kind: str, request: Request, x_init_data: Optional[str] = Header(None),
                          dev_user_id: Optional[int] = Query(None)):
    """kind: 'invite' | 'subscribe' | 'compliment'"""
    user = await get_current_user(request, x_init_data, dev_user_id)
    key_map = {"invite": "referral_bonus", "subscribe": "subscribe_bonus", "compliment": "compliment_bonus"}
    if kind not in key_map:
        raise HTTPException(status_code=400, detail="Noto'g'ri turi")
    bonus = int(await db.get_setting(key_map[kind]) or 5)
    await db.add_hearts(user["id"], bonus, "free", f"Bepul: {kind}")
    return {"ok": True, "bonus": bonus}


# =============================================================================
# ADMIN API - TO'LIQ BOSHQARUV
# =============================================================================

@app.get("/api/admin/check")
async def admin_check(request: Request, x_init_data: Optional[str] = Header(None),
                       x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    admin = await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return {"ok": True, "admin_id": ADMIN_ID, "via": admin["via"]}


@app.get("/api/admin/stats")
async def admin_stats(request: Request, x_init_data: Optional[str] = Header(None),
                       x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.get_stats()


@app.get("/api/admin/transactions")
async def admin_transactions(request: Request, x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_transactions()


# ---- Foydalanuvchilar ----

@app.get("/api/admin/users")
async def admin_list_users(request: Request, search: Optional[str] = None, x_init_data: Optional[str] = Header(None),
                            x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_users(search=search)


class UserAdjustIn(BaseModel):
    hearts_delta: Optional[int] = None
    spins_delta: Optional[int] = None
    is_vip: Optional[bool] = None
    is_banned: Optional[bool] = None


@app.post("/api/admin/users/{user_id}")
async def admin_update_user(user_id: int, body: UserAdjustIn, request: Request,
                             x_init_data: Optional[str] = Header(None),
                             x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    if body.hearts_delta is not None:
        await db.add_hearts(user_id, body.hearts_delta, "admin_adjust", "Admin tomonidan o'zgartirildi")
    if body.spins_delta is not None:
        await db.set_user_field(user_id, "spins", max(0, user["spins"] + body.spins_delta))
    if body.is_vip is not None:
        await db.set_user_field(user_id, "is_vip", int(body.is_vip))
    if body.is_banned is not None:
        await db.set_user_field(user_id, "is_banned", int(body.is_banned))
    return await db.get_user(user_id)


# ---- Reaksiyalar (yangi reaksiya qo'shish + ball belgilash) ----

class ReactionIn(BaseModel):
    emoji: str
    name: str
    cost: int = 1
    points: int = 1
    sort_order: int = 0


@app.get("/api/admin/reactions")
async def admin_list_reactions(request: Request, x_init_data: Optional[str] = Header(None),
                                x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_reactions(only_active=False)


@app.post("/api/admin/reactions")
async def admin_create_reaction(body: ReactionIn, request: Request, x_init_data: Optional[str] = Header(None),
                                 x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    rid = await db.create_reaction(body.emoji, body.name, body.cost, body.points, body.sort_order)
    return await db.get_reaction(rid)


class ReactionUpdateIn(BaseModel):
    emoji: Optional[str] = None
    name: Optional[str] = None
    cost: Optional[int] = None
    points: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


@app.put("/api/admin/reactions/{rid}")
async def admin_update_reaction(rid: int, body: ReactionUpdateIn, request: Request,
                                 x_init_data: Optional[str] = Header(None),
                                 x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    fields = {k: (int(v) if k == "is_active" else v) for k, v in body.dict(exclude_unset=True).items()}
    await db.update_reaction(rid, **fields)
    return await db.get_reaction(rid)


@app.delete("/api/admin/reactions/{rid}")
async def admin_delete_reaction(rid: int, request: Request, x_init_data: Optional[str] = Header(None),
                                 x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    await db.delete_reaction(rid)
    return {"ok": True}


# ---- Baxt g'ildiragi sovg'alari ----

class WheelPrizeIn(BaseModel):
    label: str
    hearts_reward: int
    weight: int = 10
    color: str = "#2ecc71"
    icon: str = "❤️"


@app.get("/api/admin/wheel-prizes")
async def admin_list_wheel(request: Request, x_init_data: Optional[str] = Header(None),
                            x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_wheel_prizes(only_active=False)


@app.post("/api/admin/wheel-prizes")
async def admin_create_wheel(body: WheelPrizeIn, request: Request, x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    pid = await db.create_wheel_prize(body.label, body.hearts_reward, body.weight, body.color, body.icon)
    prizes = await db.list_wheel_prizes(only_active=False)
    return next(p for p in prizes if p["id"] == pid)


class WheelPrizeUpdateIn(BaseModel):
    label: Optional[str] = None
    hearts_reward: Optional[int] = None
    weight: Optional[int] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None


@app.put("/api/admin/wheel-prizes/{pid}")
async def admin_update_wheel(pid: int, body: WheelPrizeUpdateIn, request: Request,
                              x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    fields = {k: (int(v) if k == "is_active" else v) for k, v in body.dict(exclude_unset=True).items()}
    await db.update_wheel_prize(pid, **fields)
    prizes = await db.list_wheel_prizes(only_active=False)
    return next((p for p in prizes if p["id"] == pid), None)


@app.delete("/api/admin/wheel-prizes/{pid}")
async def admin_delete_wheel(pid: int, request: Request, x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    await db.delete_wheel_prize(pid)
    return {"ok": True}


# ---- Do'kon paketlari ----

class ShopPackageIn(BaseModel):
    hearts_amount: int
    stars_price: int
    bonus_percent: int = 0
    badge: Optional[str] = None
    sort_order: int = 0


@app.get("/api/admin/shop-packages")
async def admin_list_shop(request: Request, x_init_data: Optional[str] = Header(None),
                           x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_shop_packages(only_active=False)


@app.post("/api/admin/shop-packages")
async def admin_create_shop(body: ShopPackageIn, request: Request, x_init_data: Optional[str] = Header(None),
                             x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    pid = await db.create_shop_package(body.hearts_amount, body.stars_price, body.bonus_percent,
                                        body.badge, body.sort_order)
    pkgs = await db.list_shop_packages(only_active=False)
    return next(p for p in pkgs if p["id"] == pid)


class ShopPackageUpdateIn(BaseModel):
    hearts_amount: Optional[int] = None
    stars_price: Optional[int] = None
    bonus_percent: Optional[int] = None
    badge: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


@app.put("/api/admin/shop-packages/{pid}")
async def admin_update_shop(pid: int, body: ShopPackageUpdateIn, request: Request,
                             x_init_data: Optional[str] = Header(None),
                             x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    fields = {k: (int(v) if k == "is_active" else v) for k, v in body.dict(exclude_unset=True).items()}
    await db.update_shop_package(pid, **fields)
    pkgs = await db.list_shop_packages(only_active=False)
    return next((p for p in pkgs if p["id"] == pid), None)


@app.delete("/api/admin/shop-packages/{pid}")
async def admin_delete_shop(pid: int, request: Request, x_init_data: Optional[str] = Header(None),
                             x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    await db.delete_shop_package(pid)
    return {"ok": True}


# ---- Sozlamalar (majburiy kanal, bonuslar va h.k.) ----

@app.get("/api/admin/settings")
async def admin_get_settings(request: Request, x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.get_all_settings()


class SettingsIn(BaseModel):
    settings: dict


@app.post("/api/admin/settings")
async def admin_set_settings(body: SettingsIn, request: Request, x_init_data: Optional[str] = Header(None),
                              x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    for k, v in body.settings.items():
        await db.set_setting(k, str(v))
    return await db.get_all_settings()


# ---- Xonalar ----

class RoomIn(BaseModel):
    name: str
    seats: int = 8


@app.get("/api/admin/rooms")
async def admin_list_rooms(request: Request, x_init_data: Optional[str] = Header(None),
                            x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    return await db.list_rooms()


@app.post("/api/admin/rooms")
async def admin_create_room(body: RoomIn, request: Request, x_init_data: Optional[str] = Header(None),
                             x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    rid = await db.create_room(body.name, body.seats)
    rooms = await db.list_rooms()
    return next(r for r in rooms if r["id"] == rid)


# ---- Broadcast (bot orqali barcha foydalanuvchilarga xabar) ----

class BroadcastIn(BaseModel):
    text: str


@app.post("/api/admin/broadcast")
async def admin_broadcast(body: BroadcastIn, request: Request, x_init_data: Optional[str] = Header(None),
                           x_admin_secret: Optional[str] = Header(None), dev_user_id: Optional[int] = Query(None)):
    await require_admin(request, x_init_data, x_admin_secret, dev_user_id)
    from bot_broadcast import send_broadcast  # lazy import - aiogram faqat kerak bo'lganda
    users = await db.list_users(limit=100000)
    count = await send_broadcast([u["id"] for u in users], body.text)
    return {"ok": True, "sent": count, "total": len(users)}


# =============================================================================
# STATIK FAYLLAR (Mini App + Admin panel)
# =============================================================================

app.mount("/assets", StaticFiles(directory="static"), name="assets")


@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


@app.get("/admin")
async def serve_admin():
    return FileResponse("static/admin.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
