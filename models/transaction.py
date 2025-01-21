import datetime

from sqlalchemy import Column, Integer, String, DateTime
from db.postgresql import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
