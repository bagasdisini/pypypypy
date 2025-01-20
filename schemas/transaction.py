from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    name: str
    amount: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDB(TransactionBase):
    id: int
    amount: int
    created_at: datetime
