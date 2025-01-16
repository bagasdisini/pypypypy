from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import models.provinces as models
import schemas.provinces as schemas

def create_province(db: Session, province_data: schemas.ProvinceCreate):
    try:
        province = models.Province(**province_data.model_dump())
        db.add(province)
        db.commit()
        db.refresh(province)
        return province
    except SQLAlchemyError as e:
        raise


def get_provinces(db: Session):
    try:
        return db.query(models.Province).all()
    except SQLAlchemyError as e:
        raise


def get_province_by_id(db: Session, province_id: int):
    try:
        return db.query(models.Province).filter(models.Province.id == province_id).first()
    except SQLAlchemyError as e:
        raise


def get_province_by_name(db: Session, name: str):
    try:
        return db.query(models.Province).filter(models.Province.name == name).first()
    except SQLAlchemyError as e:
        raise


def update_province(db: Session, province_id: int, province_data: schemas.ProvinceUpdate):
    try:
        province = db.query(models.Province).filter(models.Province.id == province_id).first()
        if province:
            for key, value in province_data.model_dump(exclude_unset=True).items():
                setattr(province, key, value)
            db.commit()
            db.refresh(province)
        return province
    except SQLAlchemyError as e:
        raise


def delete_province(db: Session, province_id: int):
    try:
        province = db.query(models.Province).filter(models.Province.id == province_id).first()
        if province:
            db.delete(province)
            db.commit()
        return province
    except SQLAlchemyError as e:
        raise