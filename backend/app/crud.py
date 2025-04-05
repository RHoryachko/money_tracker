from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas


def get_expenses(db: Session, user_id: int, start_date: date = None, end_date: date = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    return query.all()


def create_expense(db: Session, expense: schemas.ExpenseCreate, usd_rate: float):
    db_expense = models.Expense(
        user_id=expense.user_id,
        name=expense.name,
        date=expense.date,
        amount_uah=expense.amount_uah,
        amount_usd=expense.amount_uah / usd_rate
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    print("--------------------------------")
    print("db_expense: ", db_expense)
    print("--------------------------------")
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user_id
    ).first()
    if expense:
        db.delete(expense)
        db.commit()
        return True
    return False


def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate, usd_rate: float, user_id: int):
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user_id
    ).first()
    if db_expense:
        db_expense.name = expense.name
        db_expense.date = expense.date
        db_expense.amount_uah = expense.amount_uah
        db_expense.amount_usd = expense.amount_uah / usd_rate
        db.commit()
        db.refresh(db_expense)
        return db_expense
    return None