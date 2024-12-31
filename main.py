from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.car_route import router as car_router
from routes.garage_route import router as garage_router
from database.models import Base
from database.database import engine

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(car_router)
app.include_router(garage_router)


Base.metadata.create_all(bind=engine)
