from datetime import date
from pydantic import BaseModel, Field


class YearMonth(BaseModel):
    year:int = Field(None)
    month:str = Field(None)
    leapYear:bool = Field(None)
    monthValue:int = Field(None)


class MonthlyRequestsReportDTO(BaseModel):
     yearMonth:YearMonth= Field(None)
     requests:int = Field(None)

class CreateMaintenanceDTO(BaseModel):
    garageId: int
    carId: int
    serviceType: str
    scheduledDate: date

class UpdateMaintenanceDTO(BaseModel):
    carId:int = Field(None)
    serviceType:str = Field(None)
    scheduledDate:date = Field(None)
    garageId:int

class ResponseMaintenanceDTO(BaseModel):
     id:int = Field(None)
     carId:int = Field(None)
     carName:str = Field(None)
     serviceType:str = Field(None)
     scheduledDate:date = Field(None)
     garageId:int = Field(None)
     garageName:str = Field(None)

     class Config:
         from_attributes = True