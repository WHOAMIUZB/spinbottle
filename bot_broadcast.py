"""Admin panel orqali barcha foydalanuvchilarga ommaviy xabar yuborish."""
import asyncio
from aiogram import Bot
from config import BOT_TOKEN


async def send_broadcast(user_ids: list[int], text: str) -> int:
    bot = Bot(token=BOT_TOKEN)
    sent = 0
    try:
        for uid in user_ids:
            try:
                await bot.send_message(uid, text)
                sent += 1
                await asyncio.sleep(0.05)  # Telegram flood-limitiga tushmaslik uchun
            except Exception:
                continue
    finally:
        await bot.session.close()
    return sent
