from sqlalchemy import Integer, String, Column
from db.postgresql import Base


class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)