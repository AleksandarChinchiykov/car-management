from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from datetime import date
from pydantic import ValidationError
from database.models import Garage, Maintenance
from dtos.garage_dto import CreateGarageDTO, UpdateGarageDTO, ResponseGarageDTO, GarageDailyAvailabilityReportDTO


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

def fetch_maintenance_data(db: Session, garage_id: int, start_date: date, end_date: date) -> list:

    try:
        return (
            db.query(
                func.date(Maintenance.scheduledDate).label("report_date"),
                func.count(Maintenance.id).label("requests"),
            )
            .filter(
                Maintenance.garage_id == garage_id,
                func.date(Maintenance.scheduledDate) >= start_date,
                func.date(Maintenance.scheduledDate) <= end_date,
            )
            .group_by("report_date")
            .order_by("report_date")
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching maintenance data: {str(e)}")


def calculate_capacity(db: Session, garage_id: int, requests: int) -> int:

    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return max(garage.capacity - requests, 0)  # Ensure available capacity is not negative


def get_garage_daily_availability(
    db: Session, garage_id: int, start_date: date, end_date: date
) -> list[GarageDailyAvailabilityReportDTO]:

    maintenance_data = fetch_maintenance_data(db, garage_id, start_date, end_date)

    daily_reports = []
    for record in maintenance_data:
        daily_reports.append(
            GarageDailyAvailabilityReportDTO(
                date=record.report_date,
                requests=record.requests,
                availableCapacity=calculate_capacity(db, garage_id, record.requests),
            )
        )

    return daily_reports