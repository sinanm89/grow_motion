from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SomeClass(Base):
    __tablename__ = 'plant'
    id = Column(Integer, primary_key=True)
    measured_at = Column(DateTime(timezone=True))
    ambient_temperature = Column(Integer)
    name =  Column(String(255))
    soil_humidity =  Column(Float)
    ambient_humidity =  Column(Float)
    ambient_temperature =  Column(Float)
