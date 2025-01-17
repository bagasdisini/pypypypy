import logging
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

import crud.provinces
import schemas.provinces
import util.cache as util
from db.postgresql import get_db

provinces_router = APIRouter()


@provinces_router.post("/province", response_model=schemas.provinces.ProvinceInDB, status_code=status.HTTP_201_CREATED)
def create_province(province_data: schemas.provinces.ProvinceCreate, db: Session = Depends(get_db)):
    try:
        existing_province = crud.provinces.get_province_by_name(db, province_data.name)
        if existing_province:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already exists")

        new_province = crud.provinces.create_province(db, province_data)
        return new_province
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@provinces_router.get("/provinces", response_model=list[schemas.provinces.ProvinceInDB])
def get_provinces(db: Session = Depends(get_db)):
    try:
        cached_countries = util.get_cache("provinces")
        if cached_countries is not None:
            return cached_countries

        provinces = crud.provinces.get_provinces(db)

        util.set_cache("provinces", provinces)
        return provinces
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@provinces_router.get("/province/{province_id}", response_model=schemas.provinces.ProvinceInDB)
def get_province_by_id(province_id: int, db: Session = Depends(get_db)):
    try:
        cached_countries = util.get_cache("province"+str(province_id))
        if cached_countries is not None:
            return cached_countries

        province = crud.provinces.get_province_by_id(db, province_id)
        if province is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        util.set_cache("province"+str(province_id), province)
        return province
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@provinces_router.put("/province/{province_id}", response_model=schemas.provinces.ProvinceInDB)
def update_province(province_id: int, province_data: schemas.provinces.ProvinceUpdate, db: Session = Depends(get_db)):
    try:
        existing_province = crud.provinces.get_province_by_name(db, province_data.name)
        if existing_province and existing_province.id != province_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already exists")

        updated_province = crud.provinces.update_province(db, province_id, province_data)
        if not updated_province:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")

        return updated_province
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@provinces_router.delete("/province/{province_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_province(province_id: int, db: Session = Depends(get_db)):
    try:
        province = crud.provinces.delete_province(db, province_id)
        if not province:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found")
    except HTTPException:
            raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")