from aiogram import Router
from .start import router as start_router
from .add_expense import router as add_expense_router
from .report import router as report_router
from .delete_expense import router as delete_expense_router
from .edit_expense import router as edit_expense_router


router = Router()
router.include_router(start_router)
router.include_router(add_expense_router)
router.include_router(report_router)
router.include_router(delete_expense_router)
router.include_router(edit_expense_router)