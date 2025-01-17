from pydantic import BaseModel


class SecurityBase(BaseModel):
    string: str


class SecurityCreate(SecurityBase):
    pass


class SecurityUpdate(SecurityBase):
    pass