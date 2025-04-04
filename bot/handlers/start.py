from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Ласкаво просимо до Expense Tracker Bot! Виберіть опцію:",
        reply_markup=main_menu_kb()
    )

@router.message(Command("cancel"))
@router.message(F.text == "Cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Операція скасована. Виберіть опцію ⚙️:",
        reply_markup=main_menu_kb()
    )