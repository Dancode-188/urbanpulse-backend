from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.api.models.user import Base
from datetime import datetime

class IoTSensor(Base):
    __tablename__ = "iot_sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    last_reading = Column(DateTime, default=datetime.utcnow)
    readings = relationship("SensorReading", back_populates="sensor")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("iot_sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)
    sensor = relationship("IoTSensor", back_populates="readings")

class GISData(Base):
    __tablename__ = "gis_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    geometry = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
    properties = Column(String)  # Store as JSON string