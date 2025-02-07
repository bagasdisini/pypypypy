import schemas.transaction
import models.transaction

from sqlalchemy.orm import Session

def create_transaction(db: Session, transaction_data: schemas.transaction.TransactionSchema):
    try:
        transaction = models.transaction.Transaction(**transaction_data.model_dump())
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception as e:
        raise


def update_transaction(db: Session, transaction_id: int, transaction_data: schemas.transaction.TransactionUpdate):
    try:
        transaction = db.query(models.transaction.Transaction).filter(models.transaction.Transaction.id == transaction_id).first()
        if transaction:
            for key, value in transaction_data.model_dump().items():
                setattr(transaction, key, value)
            db.commit()
            db.refresh(transaction)
            return transaction
        else:
            raise Exception("Transaction not found")
    except Exception as e:
        raise


def create_transaction_log(db: Session, transaction_log_data: schemas.transaction.TransactionLogCreate):
    try:
        transaction_log = models.transaction.TransactionLog(**transaction_log_data.model_dump())
        db.add(transaction_log)
        db.commit()
        db.refresh(transaction_log)
        return transaction_log
    except Exception as e:
        raise