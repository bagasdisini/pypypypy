import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str
    is_active: bool


class UserInDB(UserBase):
    id: int
    password: str
    is_active: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True
        exclude_none = True
