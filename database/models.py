from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
import datetime as dt

class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

class CarGarage(Base):
    __tablename__ = 'car_and_garages'

    car_id = Column(Integer , ForeignKey('car.id',ondelete="CASCADE"), primary_key=True)
    garage_id = Column(Integer, ForeignKey('garage.id',ondelete="CASCADE"), primary_key=True)


class Garage(Base):
    __tablename__ = 'garage'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    location = Column(String)
    city = Column(String, index=True)
    capacity = Column(Integer)

    cars = relationship("Car", secondary="car_and_garages", back_populates="garages",lazy="joined",passive_deletes=True)
    maintenances = relationship("Maintenance", back_populates="garage", cascade="all, delete")

class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    make = Column(String, index=True)
    model = Column(String)
    productionYear = Column(Integer, index=True)
    licensePlate = Column(String, unique=True)

    garages = relationship("Garage",secondary="car_and_garages",lazy="joined", back_populates="cars",passive_deletes=True)
    maintenances = relationship("Maintenance", back_populates="car", cascade="all, delete")

class Maintenance(Base):
    __tablename__ = 'maintenance'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    serviceType = Column(String)
    scheduledDate = Column(DateTime, default=dt.datetime.now)
    car_id = Column(Integer, ForeignKey('car.id',ondelete="CASCADE"),nullable=False,index=True)
    garage_id = Column(Integer, ForeignKey('garage.id',ondelete="CASCADE"),nullable=False,index=True)

    car = relationship('Car', back_populates='maintenances')
    garage = relationship('Garage', back_populates='maintenances')