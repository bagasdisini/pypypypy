from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    name: str
    amount: int


class TransactionCreate(TransactionBase):
    pass


class TransactionCoreCardCreate(TransactionBase):
    token_id: str


class TransactionUpdate(TransactionBase):
    status: str
    pass


class TransactionInDB(TransactionBase):
    id: int
    amount: int
    created_at: datetime


class TransactionLogBase(BaseModel):
    transaction_id: str
    transaction_time: str
    transaction_status: str
    status_message: str
    status_code: str


class TransactionLogCreate(TransactionLogBase):
    pass


class TransactionLogUpdate(TransactionLogBase):
    pass


class TransactionLogInDB(TransactionLogBase):
    id: int
    transaction_id: str
    transaction_time: str
    transaction_status: str
    status_message: str
    status_code: str