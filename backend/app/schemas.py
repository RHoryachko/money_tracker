from pydantic import BaseModel
from datetime import date


class ExpenseBase(BaseModel):
    user_id: int
    name: str
    date: date
    amount_uah: float


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    amount_usd: float

    class Config:
        orm_mode = True