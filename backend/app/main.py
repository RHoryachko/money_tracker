import logging
import random
import pandas as pd

from io import BytesIO

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date

from app import schemas, crud, utils
from app.models import Expense
from app.database import Base, SessionLocal, engine
from app.dependencies import get_db


logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="API for managing personal expenses",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    logger.info("--------------------------------")
    logger.info("Expense: %s", expense)
    logger.info("--------------------------------")
    usd_rate = utils.get_usd_uah_rate()
    return crud.create_expense(db=db, expense=expense, usd_rate=usd_rate)


@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    return crud.get_expenses(db, start_date=start_date, end_date=end_date)


@app.get("/expenses/report/", response_class=Response)
def get_expenses_report(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    expenses = crud.get_expenses(db, start_date=start_date, end_date=end_date)
    
    logger.info("--------------------------------")
    logger.info("Expenses array: %s", expenses)
    logger.info("Expenses type: %s", type(expenses))
    logger.info("Expenses length: %s", len(expenses))
    logger.info("--------------------------------")
    
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")
    
    df = pd.DataFrame([{
        "ID": exp.id,
        "Name": exp.name,
        "Date": exp.date.strftime("%d.%m.%Y"),
        "Amount (UAH)": exp.amount_uah,
        "Amount (USD)": exp.amount_usd
    } for exp in expenses])
    
    total_uah = df["Amount (UAH)"].sum()
    total_usd = df["Amount (USD)"].sum()
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Expenses', index=False)
        pd.DataFrame({
            "Total": ["Total"],
            "Amount (UAH)": [total_uah],
            "Amount (USD)": [total_usd]
        }).to_excel(writer, sheet_name=f'Expenses {random.randint(1, 100)}', startrow=len(df)+2, index=False, header=False)
    
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=expenses_report.xlsx"}
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    if not crud.delete_expense(db, expense_id=expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    usd_rate = utils.get_usd_uah_rate()
    db_expense = crud.update_expense(db, expense_id=expense_id, expense=expense, usd_rate=usd_rate)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense