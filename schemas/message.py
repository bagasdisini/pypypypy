from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInBroker(MessageBase):
    message: str
