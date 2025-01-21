import models.users
import schemas.users

from fastapi import HTTPException
from sqlalchemy.orm import Session



def create_user(db: Session, user_data: schemas.users.UserCreate):
    user = models.users.User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.users.User).filter(models.users.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.users.User).filter(models.users.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.users.User).filter(models.users.User.email == email).first()


def update_user(db: Session, user_id: int, user_data: schemas.users.UserUpdate):
    user = db.query(models.users.User).filter(models.users.User.id == user_id).first()
    if user:
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(models.users.User).filter(models.users.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


mock_user_db = {
    "123456": {"id": "123456", "email": "user@example.com", "role": "user", "is_active": True}
}


def find_user_by_id(user_id: str):
    user = mock_user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user