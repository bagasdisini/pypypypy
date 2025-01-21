import datetime

from sqlalchemy import Column, Integer, String, DateTime
from db.postgresql import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))


class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String)
    transaction_time = Column(String)
    transaction_status = Column(String)
    status_message = Column(String)
    status_code = Column(String)