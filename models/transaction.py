import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.postgresql import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, nullable=False)
    payment_type = Column(String)
    gross_amount = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    customer_id = Column(Integer, ForeignKey("transaction_customer.id"))
    customer = relationship("Customer", back_populates="transactions")

    credit_card_id = Column(Integer, ForeignKey("transaction_credit_cards.id"))
    credit_card = relationship("CreditCard", back_populates="transaction")

    items = relationship("Item", back_populates="transaction")


class Customer(Base):
    __tablename__ = "transaction_customer"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)

    billing_address_id = Column(Integer, ForeignKey("transaction_addresses.id"))
    billing_address = relationship("Address", foreign_keys=str(billing_address_id))

    shipping_address_id = Column(Integer, ForeignKey("transaction_addresses.id"))
    shipping_address = relationship("Address", foreign_keys=str(shipping_address_id))

    transactions = relationship("Transaction", back_populates="customer")


class Address(Base):
    __tablename__ = "transaction_addresses"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country_code = Column(String, nullable=False)


class CreditCard(Base):
    __tablename__ = "transaction_credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, nullable=False)
    authentication = Column(String, default="false")
    transaction = relationship("Transaction", back_populates="credit_card", uselist=False)


class Item(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    item_id = Column(String)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    transaction = relationship("Transaction", back_populates="items")


class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String)
    fraud_status = Column(String)
    gross_amount = Column(String)
    merchant_id = Column(String)
    order_id = Column(String)
    payment_type = Column(String)
    signature_key = Column(String)
    transaction_id = Column(String)
    transaction_time = Column(String)
    transaction_status = Column(String)
    status_message = Column(String)
    status_code = Column(String)