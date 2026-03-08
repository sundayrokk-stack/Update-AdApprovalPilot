from aiogram import BaseMiddleware, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.future import select
from app.models.user import User
from app.core.config import settings

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not isinstance(event, types.Message):
            return await handler(event, data)

        session = data['session']
        user_id = event.from_user.id
        
        # Check database
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

        # 1. New user registration
        if not user:
            user = User(telegram_id=user_id, username=event.from_user.username)
            session.add(user)
            await session.commit()
            
            # Notify Admin @BlockSavvyMx
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="✅ Accept", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton(text="❌ Decline", callback_data=f"decline_{user_id}")
            ]])
            await event.bot.send_message(
                settings.ADMIN_ID, 
                f"🔔 **New Access Request**\nUser: @{event.from_user.username}\nID: `{user_id}`",
                reply_markup=kb
            )

        # 2. Enforcement
        if event.text == "/start":
            return await handler(event, data)

        if not user.is_approved:
            await event.answer(
                f"🚫 **Access Restricted**\n\nAdApprovalPilot AI is an invite-only tool. "
                f"Your access is currently pending approval.\n\nPlease contact admin: {settings.ADMIN_USERNAME}"
            )
            return

        return await handler(event, data)
