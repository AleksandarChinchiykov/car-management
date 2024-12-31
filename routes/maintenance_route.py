from calendar import isleap

from fastapi import APIRouter, Depends,Query,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import timedelta
from database.database import get_db_session
from datetime import date,datetime
from typing import Optional,List
from database.models import Maintenance
from services.maintenance_service import create_maintenance, get_maintenance_by_id, update_maintenance, \
    delete_maintenance, get_all_maintenances, delete_all_maintenances, \
    get_maintenance_monthly_requests_report
from dtos.maintenance_dto import CreateMaintenanceDTO, UpdateMaintenanceDTO, ResponseMaintenanceDTO, \
    MonthlyRequestsReportDTO, YearMonth

router = APIRouter(prefix="/maintenance", tags=["Maintenances"])

@router.post("", response_model=ResponseMaintenanceDTO)
def create(maintenance_data: CreateMaintenanceDTO, db: Session = Depends(get_db_session)):
    return create_maintenance(db, maintenance_data)

@router.get("/{id}", response_model=ResponseMaintenanceDTO)
def get_by_id(id: int, db: Session = Depends(get_db_session)):
    return get_maintenance_by_id(db, id)

@router.get("", response_model=list[ResponseMaintenanceDTO])
def get_maintenances(
    db: Session = Depends(get_db_session),
    carId: int = None,
    garageId: int = None,
    start_date: date = None,
    end_date: date = None
):
    # Pass filtering parameters to the service function
    return get_all_maintenances(db, carId, garageId, start_date, end_date)

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

@router.get("/monthlyRequestsReport", response_model=List[MonthlyRequestsReportDTO])
def get_monthly_requests_report(
    garageId: int = Query(...),
    startMonth: str = Query(...),
    endMonth: str = Query(...),
    db: Session = Depends(get_db_session)
):
    try:
        start_date = datetime.strptime(startMonth, "%Y-%m")
        end_date = datetime.strptime(endMonth, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM."
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start month cannot be after end month."
        )

    # Generate the range of months
    month_range = []
    current_date = start_date
    while current_date <= end_date:
        month_range.append((current_date.year, current_date.month))
        days_in_month = (current_date.replace(day=28) + timedelta(days=4)).day
        current_date += timedelta(days=days_in_month)
        current_date = current_date.replace(day=1)

    # Query the database for maintenance requests
    query = db.query(
        extract("year", Maintenance.scheduledDate).label("year"),
        extract("month", Maintenance.scheduledDate).label("month"),
        func.count(Maintenance.id).label("request_count")
    ).filter(
        Maintenance.scheduledDate >= start_date,
        Maintenance.scheduledDate <= end_date,
        Maintenance.garage_id == garageId
    ).group_by("year", "month").all()

    # Map query results to a dictionary for quick access
    monthly_data = {
        (int(row.year), int(row.month)): row.request_count for row in query
    }

    # Build the response
    response = []
    for year, month in month_range:
        month_enum = datetime(year, month, 1).strftime("%B").upper()
        response.append(MonthlyRequestsReportDTO(
            yearMonth=YearMonth(
                year=year,
                month=month_enum,
                leapYear=isleap(year),
                monthValue=month
            ),
            requests=monthly_data.get((year, month), 0)
        ))

    return response
