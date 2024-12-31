from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from pydantic import ValidationError
from database.models import Garage
from dtos.garage_dto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO


def create_garage(db: Session, garage_data: CreateGarageDTO) -> ResponseGarageDTO:
    new_garage = Garage(
        name=garage_data.name,
        location=garage_data.location,
        city=garage_data.city,
        capacity=garage_data.capacity,
    )
    db.add(new_garage)
    db.commit()
    db.refresh(new_garage)
    return ResponseGarageDTO.from_orm(new_garage)


def get_garages(db: Session, city: str = None) -> List[ResponseGarageDTO]:
    query = db.query(Garage)
    if city:
        query = query.filter(Garage.city.ilike(f"%{city}%"))
    garages = query.all()
    return [ResponseGarageDTO.from_orm(garage) for garage in garages]


def update_garage(db: Session, garage_id: int, garage_data: UpdateGarageDTO) -> ResponseGarageDTO:
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        return None
    for key, value in garage_data.dict(exclude_unset=True).items():
        setattr(garage, key, value)
    db.commit()
    db.refresh(garage)
    return ResponseGarageDTO.from_orm(garage)


def delete_garage(db: Session, garage_id: int) -> bool:
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        return False
    db.delete(garage)
    db.commit()
    return True

def get_all_garages(db: Session) -> list[ResponseGarageDTO]:
    try:
        garages = db.query(Garage).all()
        return [ResponseGarageDTO.model_validate(garage) for garage in garages]
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")