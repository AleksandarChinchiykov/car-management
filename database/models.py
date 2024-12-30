from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime
import datetime as dt

class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    make = Column(String, index=True)
    model = Column(String)
    productionYear = Column(Integer, index=True)
    licensePlate = Column(String, unique=True)
