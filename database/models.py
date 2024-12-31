from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
import datetime as dt

class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

class CarGarage(Base):
    __tablename__ = 'car_garages'

    car_id = Column(Integer , ForeignKey('car.id',ondelete="CASCADE"), primary_key=True)
    garage_id = Column(Integer, ForeignKey('garage.id',ondelete="CASCADE"), primary_key=True)


#using index=True we optimise the search time when filter by column
class Garage(Base):
    __tablename__ = 'garage'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String)
    location = Column(String)
    city = Column(String, index=True)
    capacity = Column(Integer)

    # reference to car class and the union(many-to_many) table car_garages
    cars = relationship("Car", secondary="car_garages", back_populates="garages",lazy="joined",passive_deletes=True)
    maintenances = relationship("Maintenance", back_populates="garage", cascade="all, delete")

class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    make = Column(String, index=True)
    model = Column(String)
    productionYear = Column(Integer, index=True)
    licensePlate = Column(String, unique=True)

    # reference to garage class and the union(many-to_many) table car_garages
    garages = relationship("Garage",secondary="car_garages",lazy="joined", back_populates="cars",passive_deletes=True)
    maintenances = relationship("Maintenance", back_populates="car", cascade="all, delete")