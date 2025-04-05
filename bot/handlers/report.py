import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile
from datetime import datetime

from services.api_client import APIClient
from keyboards.main_menu import main_menu_kb

logger = logging.getLogger(__name__)
router = Router()

class ReportStates(StatesGroup):
    waiting_for_start_date = State()
    waiting_for_end_date = State()

api_client = APIClient()

@router.message(F.text == "Отримати звіт 📊")
async def start_get_report(message: types.Message, state: FSMContext):
    await message.answer("Будь ласка, введіть початкову дату (YYYY-MM-DD) або натисніть /skip для всього часу 📅:")
    await state.set_state(ReportStates.waiting_for_start_date)


@router.message(ReportStates.waiting_for_start_date)
async def process_start_date(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(start_date=None)
    else:
        try:
            logger.info("--------------------------------")
            logger.info("Start date: %s", message.text)
            logger.info("--------------------------------")
            # Try to parse date in both formats
            try:
                start_date = datetime.strptime(message.text, "%Y-%m-%d").date()
            except ValueError:
                start_date = datetime.strptime(message.text, "%Y.%m.%d").date()
            await state.update_data(start_date=start_date)
        except ValueError:
            await message.answer("Будь ласка, введіть коректну дату в форматі YYYY-MM-DD або YYYY.MM.DD або натисніть /skip 📅.")
            return

    await message.answer("Будь ласка, введіть кінцеву дату (YYYY-MM-DD або YYYY.MM.DD) або натисніть /skip для сьогоднішньої дати 📅:")
    await state.set_state(ReportStates.waiting_for_end_date)


@router.message(ReportStates.waiting_for_end_date)
async def process_end_date(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(end_date=None)
    else:
        try:
            # Try to parse date in both formats
            try:
                end_date = datetime.strptime(message.text, "%Y-%m-%d").date()
            except ValueError:
                end_date = datetime.strptime(message.text, "%Y.%m.%d").date()
            await state.update_data(end_date=end_date)
        except ValueError:
            await message.answer("Будь ласка, введіть коректну дату в форматі YYYY-MM-DD або YYYY.MM.DD або натисніть /skip 📅.")
            return

    data = await state.get_data()
    report = await api_client.get_expenses_report(
        user_id=message.from_user.id,
        start_date=data.get("start_date"),
        end_date=data.get("end_date")
    )
    if report is None:
        await message.answer(
            "У базі не знайдено витрат. Будь ласка, додайте деякі витрати спочатку. 📝",
            reply_markup=main_menu_kb()
        )
        return
    await message.answer_document(
        BufferedInputFile(report, filename="expenses_report.xlsx"),
        reply_markup=main_menu_kb()
    )
    await state.clear() 