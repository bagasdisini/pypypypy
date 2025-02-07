import uuid
import midtransclient
import crud.transaction
import schemas.transaction
import util.string

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.config import config
from db.postgresql import get_db

transaction_router = APIRouter()


@transaction_router.post("/transaction", status_code=201)
def create_transaction(transaction_data: schemas.transaction.TransactionSchema, db: Session = Depends(get_db)):
    try:
        snap = midtransclient.Snap(
            is_production=False,
            server_key=config.MIDTRANS_SERVER_KEY
        )
        param = {
            "transaction_details": {
                "order_id": uuid.uuid4().hex,
                "gross_amount": transaction_data.gross_amount
            }, "credit_card": {
                "secure": True
            }, "customer_details": {
                "first_name": transaction_data.customer.first_name,
                "last_name": transaction_data.customer.last_name,
                "email": transaction_data.customer.email,
                "phone": transaction_data.customer.phone,
                "billing_address": {
                    "first_name": transaction_data.customer.billing_address.first_name,
                    "last_name": transaction_data.customer.billing_address.last_name,
                    "email": transaction_data.customer.billing_address.email,
                    "phone": transaction_data.customer.billing_address.phone,
                    "address": transaction_data.customer.billing_address.address,
                    "city": transaction_data.customer.billing_address.city,
                    "postal_code": transaction_data.customer.billing_address.postal_code,
                    "country_code": transaction_data.customer.billing_address.country_code
                }, "shipping_address": {
                    "first_name": transaction_data.customer.shipping_address.first_name,
                    "last_name": transaction_data.customer.shipping_address.last_name,
                    "email": transaction_data.customer.shipping_address.email,
                    "phone": transaction_data.customer.shipping_address.phone,
                    "address": transaction_data.customer.shipping_address.address,
                    "city": transaction_data.customer.shipping_address.city,
                    "postal_code": transaction_data.customer.shipping_address.postal_code,
                    "country_code": transaction_data.customer.shipping_address.country_code
                }
            }, "item_details": [
                {
                    "id": item.item_id,
                    "price": item.price,
                    "quantity": item.quantity,
                    "name": item.name
                } for item in transaction_data.items
            ]
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

@transaction_router.post("/transaction/core/card", status_code=201)
def create_transaction(transaction_data: schemas.transaction.TransactionCreate, db: Session = Depends(get_db)):
    try:
        core_api = midtransclient.CoreApi(
            is_production=False,
            server_key=config.MIDTRANS_SERVER_KEY,
            client_key=config.MIDTRANS_CLIENT_KEY
        )

        param = {
            "payment_type": "credit_card",
            "transaction_details": {
                "order_id": uuid.uuid4().hex,
                "gross_amount": transaction_data.amount
            }, "credit_card": {
                "token_id": 'CREDIT_CARD_TOKEN',
                "authentication": True
            }, "customer_details": {
                "first_name": transaction_data.name,
                "last_name": util.string.random_string(5),
                "email": util.string.random_string(5) + "@example.com",
                "phone": "08111222333"
            }
        }

        transaction = core_api.charge(param)

        transaction_token = transaction['status_code']
        if transaction_token != '200' or transaction_token != '201':
            raise HTTPException(status_code=500, detail="Failed to create transaction")

        crud.transaction.create_transaction(db, transaction_data)

        return transaction
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@transaction_router.post("/transaction/webhook", status_code=201)
def webhook_notification(webhook_data: schemas.transaction.TransactionLogCreate, db: Session = Depends(get_db)):
    try:
        crud.transaction.create_transaction_log(db, webhook_data)
        return webhook_data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")