"""Plant information model."""
from sqlalchemy import Column, Integer, String, Float, DateTime

from generic_model import Base


class Plant(Base):
    """Main plant database."""

    __tablename__ = 'plant'
    id = Column(Integer, primary_key=True)
    measured_at = Column(DateTime(timezone=True))
    ambient_temperature = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    soil_humidity = Column(Float, nullable=True)
    ambient_humidity = Column(Float, nullable=True)
    ambient_temperature = Column(Float, nullable=True)
