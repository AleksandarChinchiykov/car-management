from sqlalchemy.orm import Session
from typing import List
from database.models import Car
from dtos.car_dto import CreateCarDTO, UpdateCarDTO, ResponseCarDTO


def create_car(db: Session, car_data: CreateCarDTO) -> ResponseCarDTO:
    new_car = Car(
        make=car_data.make,
        model=car_data.model,
        productionYear=car_data.productionYear,
        licensePlate=car_data.licensePlate,
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return ResponseCarDTO.from_orm(new_car)


def get_cars(db: Session, make: str = None, from_year: int = None, to_year: int = None) -> List[ResponseCarDTO]:
    query = db.query(Car)
    if make:
        query = query.filter(Car.make.ilike(f"%{make}%"))
    if from_year:
        query = query.filter(Car.productionYear >= from_year)
    if to_year:
        query = query.filter(Car.productionYear <= to_year)
    cars = query.all()
    return [ResponseCarDTO.from_orm(car) for car in cars]


def update_car(db: Session, car_id: int, car_data: UpdateCarDTO) -> ResponseCarDTO:
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return None
    for key, value in car_data.dict(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return ResponseCarDTO.from_orm(car)


def delete_car(db: Session, car_id: int) -> bool:
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return False
    db.delete(car)
    db.commit()
    return True
