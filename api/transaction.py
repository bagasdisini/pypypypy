import uuid

import midtransclient
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud.transaction
import schemas.transaction
import util.string
from core.config import config
from db.postgresql import get_db

transaction_router = APIRouter()


@transaction_router.post("/transaction", status_code=201)
def create_transaction(transaction_data: schemas.transaction.TransactionCreate, db: Session = Depends(get_db)):
    try:
        snap = midtransclient.Snap(
            is_production=False,
            server_key=config.MIDTRANS_SERVER_KEY
        )
        param = {
            "transaction_details": {
                "order_id": uuid.uuid4().hex,
                "gross_amount": transaction_data.amount
            }, "credit_card": {
                "secure": True
            }, "customer_details": {
                "first_name": transaction_data.name,
                "last_name": util.string.random_string(5),
                "email": util.string.random_string(5)+"@example.com",
                "phone": "08111222333"
            }
        }

        transaction = snap.create_transaction(param)

        transaction_token = transaction['token']
        if not transaction_token:
            raise HTTPException(status_code=500, detail="Failed to create transaction")

        crud.transaction.create_transaction(db, transaction_data)

        return transaction
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")