from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db_session
from dtos.garage_dto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO
from services.garage_service import create_garage, get_garages, update_garage, delete_garage

router = APIRouter(prefix="/garages", tags=["Garages"])


@router.post("/", response_model=ResponseGarageDTO)
def create_garage_endpoint(garage_data: CreateGarageDTO, db: Session = Depends(get_db_session)):
    return create_garage(db, garage_data)


@router.get("/", response_model=list[ResponseGarageDTO])
def get_garages_endpoint(city: str = None, db: Session = Depends(get_db_session)):
    return get_garages(db, city)


@router.put("/{garage_id}", response_model=ResponseGarageDTO)
def update_garage_endpoint(garage_id: int, garage_data: UpdateGarageDTO, db: Session = Depends(get_db_session)):
    garage = update_garage(db, garage_id, garage_data)
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage


@router.delete("/{garage_id}", response_model=dict)
def delete_garage_endpoint(garage_id: int, db: Session = Depends(get_db_session)):
    success = delete_garage(db, garage_id)
    if not success:
        raise HTTPException(status_code=404, detail="Garage not found")
    return {"message": "Garage deleted successfully"}
