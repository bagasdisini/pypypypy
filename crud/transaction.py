import schemas.transaction
import models.transaction

from sqlalchemy.orm import Session

def create_transaction(db: Session, transaction_data: schemas.transaction.TransactionCreate):
    try:
        transaction = models.transaction.Transaction(**transaction_data.model_dump())
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception as e:
        raise