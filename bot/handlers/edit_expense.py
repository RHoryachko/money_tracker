import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile

from services.api_client import APIClient
from keyboards.main_menu import main_menu_kb


router = Router()

logger = logging.getLogger(__name__)

class EditExpenseStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_name = State()
    waiting_for_amount = State()


api_client = APIClient()


@router.message(F.text == "Редагувати витрату 📝")
async def start_edit_expense(message: types.Message, state: FSMContext):
    report = await api_client.get_expenses_report(user_id=message.from_user.id)
    if report is None:
        await message.answer(
            "У базі не знайдено витрат. Будь ласка, додайте деякі витрати спочатку. 📝",
            reply_markup=main_menu_kb()
        )
        return
    await message.answer_document(
        BufferedInputFile(report, filename="all_expenses.xlsx")
    )
    await message.answer("Будь ласка, введіть ID витрати, яку хочете редагувати 📝:")
    await state.set_state(EditExpenseStates.waiting_for_id)


@router.message(EditExpenseStates.waiting_for_id)
async def process_expense_id(message: types.Message, state: FSMContext):
    try:
        expense_id = int(message.text)
        await state.update_data(expense_id=expense_id)
        await message.answer("Будь ласка, введіть нову назву для витрати 📝:")
        await state.set_state(EditExpenseStates.waiting_for_name)
    except ValueError:
        await message.answer("Будь ласка, введіть коректний цілий ID. 🔢")


@router.message(EditExpenseStates.waiting_for_name)
async def process_expense_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Будь ласка, введіть нову суму в гривнях 💰:")
    await state.set_state(EditExpenseStates.waiting_for_amount)


@router.message(EditExpenseStates.waiting_for_amount)
async def process_edit_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
        
        data = await state.get_data()
        response = await api_client.update_expense(
            user_id=message.from_user.id,
            expense_id=data['expense_id'],
            name=data['name'],
            amount=amount
        )

        logger.info("--------------------------------")
        logger.info("Response: %s", response)
        logger.info("--------------------------------")

        if isinstance(response, dict) and 'detail' in response:
            await message.answer("Витрата з таким ID не знайдена. Будь ласка, спробуйте ще раз. 🔍")
            return
        
        await message.answer(
            f"Витрата успішно оновлена!\n"
            f"Назва: {data['name']}\n"
            f"Сума: {amount} UAH",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    except ValueError:
        await message.answer("Будь ласка, введіть коректну позитивну суму 💰.")


def register_edit_expense_handlers(dp):
    dp.register_message_handler(start_edit_expense, text="Edit Expense", state="*")
    dp.register_message_handler(process_expense_id, state=EditExpenseStates.waiting_for_id)
    dp.register_message_handler(process_expense_name, state=EditExpenseStates.waiting_for_name)
    dp.register_message_handler(process_edit_amount, state=EditExpenseStates.waiting_for_amount)