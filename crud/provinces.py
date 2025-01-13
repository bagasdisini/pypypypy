from sqlalchemy.orm import Session

import models.provinces as models
import schemas.provinces as schemas

def create_province(db: Session, province_data: schemas.ProvinceCreate):
    province = models.Province(**province_data.model_dump())
    db.add(province)
    db.commit()
    db.refresh(province)
    return province

def get_provinces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Province).offset(skip).limit(limit).all()

def get_province_by_id(db: Session, province_id: int):
    return db.query(models.Province).filter(models.Province.id == province_id).first()

def get_province_by_name(db: Session, name: str):
    return db.query(models.Province).filter(models.Province.name == name).first()

def update_province(db: Session, province_id: int, province_data: schemas.ProvinceUpdate):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province:
        for key, value in province_data.model_dump().items():
            setattr(province, key, value)
        db.commit()
        db.refresh(province)
    return province

def delete_province(db: Session, province_id: int):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province:
        db.delete(province)
        db.commit()
    return province