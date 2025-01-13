from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud.provinces
import schemas.provinces
import util.string
from db.postgresql import get_db


provinces_router = APIRouter()


@provinces_router.post("/province", response_model=schemas.provinces.ProvinceInDB)
def create_province(province_data: schemas.provinces.ProvinceCreate, db: Session = Depends(get_db)):
    existing_province = crud.provinces.get_province_by_name(db, province_data.name)
    if existing_province:
        raise HTTPException(status_code=400, detail="Name already exists")
    try:
        province_data.password = util.string.hash_password(province_data.password)
        return crud.provinces.create_province(db, province_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@provinces_router.get("/provinces", response_model=list[schemas.provinces.ProvinceInDB])
def get_provinces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.provinces.get_provinces(db, skip, limit)


@provinces_router.get("/province/{province_id}", response_model=schemas.provinces.ProvinceInDB)
def get_province_by_id(province_id: int, db: Session = Depends(get_db)):
    try:
        province = crud.provinces.get_province_by_id(db, province_id)
        if not province:
            raise HTTPException(status_code=404, detail="Province not found")
        return province
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@provinces_router.put("/province/{province_id}", response_model=schemas.provinces.ProvinceInDB)
def update_province(province_id: int, province_data: schemas.provinces.ProvinceUpdate, db: Session = Depends(get_db)):
    province = crud.provinces.update_province(db, province_id, province_data)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    return province


@provinces_router.delete("/province/{province_id}", response_model=schemas.provinces.ProvinceInDB)
def delete_province(province_id: int, db: Session = Depends(get_db)):
    province = crud.provinces.delete_province(db, province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    return province
