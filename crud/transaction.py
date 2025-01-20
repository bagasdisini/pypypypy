from sqlalchemy.orm import Session
import schemas.transaction as schemas
import models.transaction as models

def create_transaction(db: Session, transaction_data: schemas.TransactionCreate):
    try:
        transaction = models.Transaction(**transaction_data.model_dump())
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception as e:
        raise