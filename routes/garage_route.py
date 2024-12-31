from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db_session
from datetime import date
from dtos.garage_dto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO, GarageDailyAvailabilityReportDTO
from services.garage_service import create_garage, get_garages, update_garage, delete_garage, \
    get_garage_daily_availability

router = APIRouter(prefix="/garages", tags=["Garages"])



@router.get("/dailyAvailabilityReport", response_model=list[GarageDailyAvailabilityReportDTO])
def get_garage_availability_endpoint(
    garageId: int,
    startDate: date,
    endDate: date,
    db: Session = Depends(get_db_session),
):
    garage_id = garageId
    start_date = startDate
    end_date = endDate

    if start_date > end_date:
        raise HTTPException(status_code=422, detail="Start date cannot be after end date")

    return get_garage_daily_availability(db, garage_id, start_date, end_date)

@router.post("", response_model=ResponseGarageDTO)
def create_garage_endpoint(garage_data: CreateGarageDTO, db: Session = Depends(get_db_session)):
    return create_garage(db, garage_data)


@router.get("", response_model=list[ResponseGarageDTO])
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
