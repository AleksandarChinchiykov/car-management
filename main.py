# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.car_route import router as car_router
from routes.garage_route import router as garage_router
from routes.maintenance_route import router as maintenance_router
from database.models import Base
from database.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Include routers
app.include_router(car_router)
app.include_router(garage_router)
app.include_router(maintenance_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Management API!"}
