import logging
import random
import pandas as pd
import xlsxwriter

from io import BytesIO

from fastapi import FastAPI, Depends, HTTPException, Response, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app import schemas, crud, utils
from app.models import Expense
from app.database import Base, SessionLocal, engine
from app.dependencies import get_db
from app.config import settings


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


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_secret_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    logger.info("--------------------------------")
    logger.info("Expense: %s", expense)
    logger.info("--------------------------------")
    usd_rate = utils.get_usd_uah_rate()
    return crud.create_expense(db=db, expense=expense, usd_rate=usd_rate)


@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return crud.get_expenses(db, user_id=user_id, start_date=start_date, end_date=end_date)


@app.get("/expenses/report/")
async def get_expenses_report(
    user_id: int = Query(...),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    expenses = crud.get_expenses(db, user_id=user_id, start_date=start_date, end_date=end_date)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")
        
    # Create Excel report
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    # Write headers
    headers = ["ID", "Name", "Date", "Amount (UAH)", "Amount (USD)"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Write data
    for row, expense in enumerate(expenses, start=1):
        worksheet.write(row, 0, expense.id)
        worksheet.write(row, 1, expense.name)
        worksheet.write(row, 2, expense.date.strftime("%Y-%m-%d"))
        worksheet.write(row, 3, expense.amount_uah)
        worksheet.write(row, 4, expense.amount_usd)
    
    workbook.close()
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=expenses_report.xlsx"}
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    if crud.delete_expense(db, expense_id, user_id):
        return {"success": True, "message": "Expense deleted successfully"}
    return {"success": False, "message": "Expense not found"}


@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    usd_rate = utils.get_usd_uah_rate()
    updated_expense = crud.update_expense(db, expense_id, expense, usd_rate, expense.user_id)
    if updated_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense