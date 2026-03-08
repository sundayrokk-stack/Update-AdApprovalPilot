from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.core.config import settings
from app.services.audit_engine import run_audit

router = Router()

class AuditState(StatesGroup):
    choosing_issue = State()
    providing_link = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"🚀 **Welcome to AdApprovalPilot AI**\n\n"
        "Your Telegram Ads compliance & channel audit assistant.\n\n"
        f"Admin: {settings.ADMIN_USERNAME}\n"
        "Status: System Active 🟢",
        parse_mode="Markdown"
    )

@router.message(F.text == "Start Audit")
async def start_audit(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="Declined: Destination Quality")],
        [types.KeyboardButton(text="Ads in review too long")],
        [types.KeyboardButton(text="General Compliance Check")]
    ], resize_keyboard=True)
    await message.answer("What issue are you facing?", reply_markup=kb)
    await state.set_state(AuditState.choosing_issue)

@router.message(AuditState.choosing_issue)
async def process_issue(message: types.Message, state: FSMContext):
    await state.update_data(issue=message.text)
    await message.answer("Please provide your Channel Link, Bot Link, or Profile link (e.g., t.me/username):")
    await state.set_state(AuditState.providing_link)

@router.message(AuditState.providing_link)
async def perform_audit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    results = await run_audit(message.text, data['issue'])
    await message.answer(results, parse_mode="Markdown")
    await state.clear()
