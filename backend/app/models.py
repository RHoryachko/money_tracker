from sqlalchemy import Column, Integer, String, Date, Float

from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    amount_uah = Column(Float)
    amount_usd = Column(Float)