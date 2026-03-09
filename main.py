import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.routers.bot_router import router as bot_router
from app.middleware.auth import AuthMiddleware
from database import AsyncSessionLocal

app = FastAPI()
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Inject DB session into middleware
@dp.update.outer_middleware()
async def db_session_middleware(handler, event, data):
    async with AsyncSessionLocal() as session:
        data['session'] = session
        return await handler(event, data)

dp.message.middleware(AuthMiddleware())
dp.include_router(bot_router)

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(f"{settings.RENDER_EXTERNAL_URL}/webhook")

@app.post("/webhook")
async def telegram_webhook(update: dict):
    from aiogram.types import Update
    await dp.feed_update(bot, Update(**update))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
