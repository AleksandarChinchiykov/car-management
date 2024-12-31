from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from datetime import date
from dtos.car_dto import ResponseCarDTO
from dtos.garage_dto import ResponseGarageDTO
from database.models import Maintenance, Car, Garage
from dtos.maintanance_dto import CreateMaintenanceDTO,UpdateMaintenanceDTO,ResponseMaintenanceDTO

def create_maintenance(db: Session, maintenance_data: CreateMaintenanceDTO) -> ResponseMaintenanceDTO:
    try:
        car = db.query(Car).filter(Car.id == maintenance_data.carId).first()
        garage = db.query(Garage).filter(Garage.id == maintenance_data.garageId).first()

        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        if not garage:
            raise HTTPException(status_code=404, detail="Garage not found")

        new_maintenance = Maintenance(
            car_id=maintenance_data.carId,
            garage_id=maintenance_data.garageId,
            serviceType=maintenance_data.serviceType,
            scheduledDate=maintenance_data.scheduledDate
        )

        db.add(new_maintenance)
        db.commit()
        db.refresh(new_maintenance)

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=new_maintenance.id,
            carId=new_maintenance.car_id,
            carName=car_name,
            serviceType=new_maintenance.serviceType,
            scheduledDate=new_maintenance.scheduledDate,
            garageId=new_maintenance.garage_id,
            garageName=garage.name
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_maintenance_by_id(db: Session, maintenance_id: int) -> ResponseMaintenanceDTO:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")

        car = db.query(Car).filter(Car.id == maintenance.car_id).first()
        garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()

        if not car or not garage:
            raise HTTPException(status_code=404, detail="Car or Garage not found")

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.car_id,
            carName=car_name,
            serviceType=maintenance.serviceType,
            scheduledDate=maintenance.scheduledDate,
            garageId=maintenance.garage_id,
            garageName=garage.name
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def update_maintenance(db: Session, maintenance_id: int, maintenance_data: UpdateMaintenanceDTO) -> ResponseMaintenanceDTO:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")

        for key, value in maintenance_data.model_dump(exclude_unset=True).items():
            if key == 'carId':
                maintenance.car_id = value
            elif key == 'garageId':
                maintenance.garage_id = value
            else:
                setattr(maintenance, key, value)

        db.commit()
        db.refresh(maintenance)
        print(f"Updated maintenance: {maintenance.id}, {maintenance.car_id}, {maintenance.serviceType}")

        car = db.query(Car).filter(Car.id == maintenance.car_id).first()
        garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()

        if not car or not garage:
            raise HTTPException(status_code=404, detail="Car or Garage not found")

        car_name = f"{car.make} {car.model}"

        return ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.car_id,
            carName=car_name,
            serviceType=maintenance.serviceType,
            scheduledDate=maintenance.scheduledDate,
            garageId=maintenance.garage_id,
            garageName=garage.name
        )

    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")


def delete_maintenance(db: Session, maintenance_id: int) -> None:
    try:
        maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
        if not maintenance:
            raise HTTPException(status_code=404, detail="Resource not found")

        db.delete(maintenance)
        db.commit()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Bad request")

def get_all_maintenances(db: Session,car_id: int,garage_id: int,start_date: date,end_date: date) -> ResponseMaintenanceDTO:
    query = db.query(Maintenance)

    if car_id:
        query = query.filter(Maintenance.car_id == car_id)

    if garage_id:
        query = query.filter(Maintenance.garage_id == garage_id)

    if start_date:
        query = query.filter(Maintenance.scheduledDate >= start_date)

    if end_date:
        query = query.filter(Maintenance.scheduledDate <= end_date)

    maintenances = query.all()
    if not maintenances:
        raise HTTPException(status_code=404, detail="No maintenances found")

    response = []
    for maintenance in maintenances:
        car = db.query(Car).filter(Car.id == maintenance.car_id).first()
        garage = db.query(Garage).filter(Garage.id == maintenance.garage_id).first()

        if not car or not garage:
            raise HTTPException(status_code=404, detail=f"Car or Garage not found for maintenance ID {maintenance.id}")

        car_name = f"{car.make} {car.model}"

        maintenance_response = ResponseMaintenanceDTO(
            id=maintenance.id,
            carId=maintenance.car_id,
            carName=car_name,
            serviceType=maintenance.serviceType,
            scheduledDate=maintenance.scheduledDate,
            garageId=maintenance.garage_id,
            garageName=garage.name
        )
        response.append(maintenance_response)

    return response

def delete_all_maintenances(db: Session) -> None:
    try:
        db.query(Maintenance).delete()
        db.commit()
        print("All maintenances deleted successfully.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting maintenances: {str(e)}")