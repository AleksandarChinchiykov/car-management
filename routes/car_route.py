from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db_session
from dtos.car_dto import CreateCarDTO, UpdateCarDTO, ResponseCarDTO
from services.car_service import create_car, get_cars, update_car, delete_car,get_car_by_id

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("/", response_model=ResponseCarDTO)
def create_car_endpoint(car_data: CreateCarDTO, db: Session = Depends(get_db_session)):
    return create_car(db, car_data)


@router.get("/", response_model=list[ResponseCarDTO])
def get_cars_endpoint(make: str = None, garage: str = None, from_year: int = None, to_year: int = None, db: Session = Depends(get_db_session)):
    return get_cars(db, make, garage, from_year, to_year)

@router.get("/{car_id}", response_model=ResponseCarDTO)
def get_car_by_id_endpoint(car_id: int, db: Session = Depends(get_db_session)):
    car = get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/{car_id}", response_model=ResponseCarDTO)
def update_car_endpoint(car_id: int, car_data: UpdateCarDTO, db: Session = Depends(get_db_session)):
    car = update_car(db, car_id, car_data)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.delete("/{car_id}", response_model=dict)
def delete_car_endpoint(car_id: int, db: Session = Depends(get_db_session)):
    success = delete_car(db, car_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
