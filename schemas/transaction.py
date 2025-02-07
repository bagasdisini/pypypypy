from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class AddressSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str
    city: str
    postal_code: str
    country_code: str

    class Config:
        from_attributes = True


class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    billing_address: Optional[AddressSchema] = None
    shipping_address: Optional[AddressSchema] = None

    class Config:
        from_attributes = True


class CreditCardSchema(BaseModel):
    token_id: str
    authentication: bool

    class Config:
        from_attributes = True


class ItemSchema(BaseModel):
    item_id: str
    name: str
    price: int
    quantity: int

    class Config:
        from_attributes = True


class TransactionSchema(BaseModel):
    payment_type: str
    gross_amount: int
    status: str = "pending"
    created_at: datetime
    customer: CustomerSchema
    credit_card: CreditCardSchema
    items: List[ItemSchema]

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    name: str
    amount: int


class TransactionCreate(TransactionBase):
    pass


class TransactionCoreCardCreate(TransactionBase):
    token_id: str


class TransactionUpdate(TransactionBase):
    status: str
    pass


class TransactionInDB(TransactionBase):
    id: int
    amount: int
    created_at: datetime


class TransactionLogBase(BaseModel):
    currency: str
    fraud_status: str
    gross_amount: str
    merchant_id: str
    order_id: str
    payment_type: str
    signature_key: str
    transaction_id: str
    transaction_time: str
    transaction_status: str
    status_message: str
    status_code: str


class TransactionLogCreate(TransactionLogBase):
    pass


class TransactionLogUpdate(TransactionLogBase):
    pass


class TransactionLogInDB(TransactionLogBase):
    id: int
    transaction_id: str
    transaction_time: str
    transaction_status: str
    status_message: str
    status_code: str