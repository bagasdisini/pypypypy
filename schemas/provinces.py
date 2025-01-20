from pydantic import BaseModel


class ProvinceBase(BaseModel):
    name: str


class ProvinceCreate(ProvinceBase):
    pass


class ProvinceUpdate(ProvinceBase):
    pass


class ProvinceInDB(ProvinceBase):
    id: int
    name: str