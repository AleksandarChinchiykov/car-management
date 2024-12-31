from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db_session
from datetime import date
from services.maintanance_service import create_maintenance, get_maintenance_by_id, update_maintenance, \
    delete_maintenance, get_all_maintenances, delete_all_maintenances
from dtos.maintanance_dto import CreateMaintenanceDTO, UpdateMaintenanceDTO, ResponseMaintenanceDTO

router = APIRouter(prefix="/maintenances", tags=["Maintenances"])

@router.post("/", response_model=ResponseMaintenanceDTO)
def create(maintenance_data: CreateMaintenanceDTO, db: Session = Depends(get_db_session)):
    return create_maintenance(db, maintenance_data)

@router.get("/{id}", response_model=ResponseMaintenanceDTO)
def get_by_id(id: int, db: Session = Depends(get_db_session)):
    return get_maintenance_by_id(db, id)

@router.get("/", response_model=list[ResponseMaintenanceDTO])
def get_maintenances(
    db: Session = Depends(get_db_session),
    car_id: int = None,
    garage_id: int = None,
    start_date: date = None,
    end_date: date = None
):
    # Pass filtering parameters to the service function
    return get_all_maintenances(db, car_id, garage_id, start_date, end_date)

@router.put("/{id}", response_model=ResponseMaintenanceDTO)
def update(id: int, maintenance_data: UpdateMaintenanceDTO, db: Session = Depends(get_db_session)):
    return update_maintenance(db, id, maintenance_data)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db_session)):
    delete_maintenance(db, id)
    return {"detail": "Resource deleted"}

@router.delete("")
def delete_maintenances(db:Session = Depends(get_db_session)):
    return delete_all_maintenances(db)