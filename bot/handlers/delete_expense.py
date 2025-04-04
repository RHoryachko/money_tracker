import logging
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile
from io import BytesIO
from services.api_client import APIClient
from keyboards.main_menu import main_menu_kb

logger = logging.getLogger(__name__)
router = Router()

class DeleteExpenseStates(StatesGroup):
    waiting_for_id = State()

api_client = APIClient()

@router.message(F.text == "Видалити витрату 🗑")
async def start_delete_expense(message: types.Message, state: FSMContext):
    report = await api_client.get_expenses_report()
    logger.info("--------------------------------")
    logger.info("Report content: %s", report)
    logger.info("Report type: %s", type(report))
    logger.info("--------------------------------")
    
    try:
        if report.get("status_code") == 404:
            
            await message.answer(
                "У базі не знайдено витрат. Будь ласка, додайте деякі витрати спочатку. 📝",
                reply_markup=main_menu_kb()
            )
            return
    except:
        pass
    
    await message.answer_document(
        BufferedInputFile(report, filename="all_expenses.xlsx")
    )
    await message.answer("Будь ласка, введіть ID витрати, яку хочете видалити 🗑:")
    await state.set_state(DeleteExpenseStates.waiting_for_id)

@router.message(DeleteExpenseStates.waiting_for_id)
async def process_expense_id(message: types.Message, state: FSMContext):
    try:
        expense_id = int(message.text)
        success = await api_client.delete_expense(expense_id)
        if success:
            await message.answer("Витрата успішно видалена! 🗑", reply_markup=main_menu_kb())
        else:
            await message.answer("Не вдалося видалити витрату. Будь ласка, перевірте ID. ❌", reply_markup=main_menu_kb())
        await state.clear()
    except ValueError:
        await message.answer("Будь ласка, введіть коректний цілий ID. 🔢")

def register_delete_expense_handlers(dp):
    dp.register_message_handler(start_delete_expense, text="Delete Expense", state="*")
    dp.register_message_handler(process_expense_id, state=DeleteExpenseStates.waiting_for_id)