from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from geojson_pydantic import Point, Geometry

class SensorReadingBase(BaseModel):
    value: float
    timestamp: Optional[datetime] = None

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReading(SensorReadingBase):
    id: int
    sensor_id: int

    class Config:
        orm_mode = True

class IoTSensorBase(BaseModel):
    name: str
    type: str
    location: Point

class IoTSensorCreate(IoTSensorBase):
    pass

class IoTSensor(IoTSensorBase):
    id: int
    last_reading: datetime
    readings: List[SensorReading] = []

    class Config:
        orm_mode = True

class GISDataBase(BaseModel):
    name: str
    type: str
    geometry: Geometry
    properties: dict

class GISDataCreate(GISDataBase):
    pass

class GISData(GISDataBase):
    id: int

    class Config:
        orm_mode = True


