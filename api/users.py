import crud.users
import schemas.users
import util.string

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.postgresql import get_db
from util.jwt import jwt
from util.jwt.jwt import get_current_user

users_router = APIRouter()


@users_router.post("/user", response_model=schemas.users.UserInDB, status_code=201)
def create_user(user_data: schemas.users.UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = crud.users.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        existing_email = crud.users.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

        user_data.password = util.string.hash_password(user_data.password)

        return crud.users.create_user(db, user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@users_router.get("/users", response_model=list[schemas.users.UserInDB], status_code=200)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.users.get_users(db, skip, limit)


@users_router.get("/user/{user_id}", response_model=schemas.users.UserInDB, status_code=200)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = crud.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@users_router.put("/user/{user_id}", response_model=schemas.users.UserInDB)
def update_user(user_id: int, user_data: schemas.users.UserUpdate, db: Session = Depends(get_db)):
    user = crud.users.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.delete("/user/{user_id}", response_model=schemas.users.UserInDB)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.users.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.get("/me")
async def get_me(current_user: jwt.UserClaims = Depends(get_current_user)):
    user = crud.users.find_user_by_id(current_user.id)
    if not user["is_active"]:
        raise HTTPException(status_code=401, detail="User is not active")
    return {"id": user["id"], "email": user["email"], "role": user["role"]}