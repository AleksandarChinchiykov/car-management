from datetime import date

from pydantic import BaseModel, Field


class ResponseGarageDTO(BaseModel):
    id: int
    name:str
    location: str
    city: str
    capacity: int

    class Config:
        from_attributes = True

class CreateGarageDTO(BaseModel):
    name:str
    location:str
    city:str
    capacity:int

class UpdateGarageDTO(BaseModel):
    name: str = Field(None)
    location: str = Field(None)
    city: str = Field(None)
    capacity: int = Field(None)

class GarageDailyAvailabilityReportDTO(BaseModel):
    date: date
    requests: int
    availableCapacity: int

    class Config:
        from_attributes = True

