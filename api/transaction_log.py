import crud.transaction
import schemas.transaction

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.postgresql import get_db

transaction_log_router = APIRouter()


@transaction_log_router.post("/transaction-log", status_code=201)
def create_transaction_log(transaction_log_data: schemas.transaction.TransactionLogCreate, db: Session = Depends(get_db)):
    try:
        return crud.transaction.create_transaction_log(db, transaction_log_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")