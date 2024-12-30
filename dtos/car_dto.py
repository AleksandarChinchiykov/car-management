from pydantic import BaseModel, Field

class CreateCarDTO(BaseModel):
    make:str = Field(None)
    model:str = Field(None)
    productionYear: int = Field(None)
    licensePlate:str = Field(None)

class UpdateCarDTO(BaseModel):
    make:str = Field(None)
    model:str = Field(None)
    productionYear: int = Field(None)
    licensePlate:str = Field(None)

class ResponseCarDTO(BaseModel):
    id:int = Field(None)
    make:str = Field(None)
    model:str = Field(None)
    productionYear: int = Field(None)
    licensePlate:str = Field(None)
