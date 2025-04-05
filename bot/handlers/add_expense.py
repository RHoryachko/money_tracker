from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from services.api_client import APIClient
from keyboards.main_menu import main_menu_kb


router = Router()
api_client = APIClient()

class AddExpenseStates(StatesGroup):
    name = State()
    date = State()
    amount = State()


@router.message(F.text == "Додати витрату 💰")
async def start_add_expense(message: Message, state: FSMContext):
    await message.answer("Будь ласка, введіть назву витрати 📝:")
    await state.set_state(AddExpenseStates.name)

@router.message(AddExpenseStates.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Будь ласка, введіть дату в форматі dd.mm.YYYY 📅:")
    await state.set_state(AddExpenseStates.date)

@router.message(AddExpenseStates.date)
async def process_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y").date()
        await state.update_data(date=date)
        await message.answer("Будь ласка, введіть суму в гривнях 💰:")
        await state.set_state(AddExpenseStates.amount)
    except ValueError:
        await message.answer("Неправильний формат дати. Будь ласка, використовуйте формат dd.mm.YYYY 📅.")

@router.message(AddExpenseStates.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
        
        data = await state.get_data()
        response = await api_client.create_expense(
            user_id=message.from_user.id,
            name=data['name'],
            date=data['date'],
            amount=amount
        )
        
        await message.answer(
            f"Витрата успішно додана!\n"
            f"Назва: {data['name']}\n"
            f"Дата: {data['date'].strftime('%d.%m.%Y')}\n"
            f"Сума: {amount} UAH",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    except ValueError:
        await message.answer("Будь ласка, введіть коректну позитивну суму 💰.")