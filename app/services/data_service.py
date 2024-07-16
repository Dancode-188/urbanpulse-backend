from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.data import IoTSensor, SensorReading, GISData
from app.api.schemas.data import IoTSensorCreate, SensorReadingCreate, GISDataCreate
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

async def get_iot_sensor(db: AsyncSession, sensor: IoTSensorCreate):
    db_sensor = IoTSensor(
        name=sensor.name,
        type=sensor.type,
        location=from_shape(shape(sensor.location))
    )
    db.add(db_sensor)
    await db.commit()
    await db.refresh(db_sensor)
    return db_sensor

async def create_sensor_reading(db: AsyncSession, reading: SensorReadingCreate, sensor_id: int):
    db_reading = SensorReading(
        sensor_id=sensor_id,
        value=reading.value,
        timestamp=reading.timestamp
    )
    db.add(db_reading)
    await db.commit()
    await db.refresh(db_reading)
    return db_reading

async def get_gis_data(db: AsyncSession, gis_data: GISDataCreate):
    db_gis_data = GISData(
        name=gis_data.name,
        type=gis_data.type,
        geometry=from_shape(shape(gis_data.geometry)),
        properties=str(gis_data.properties)
    )
    db.add(db_gis_data)
    await db.commit()
    await db.refresh(db_gis_data)
    return db_gis_data

async def get_iot_sensors(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(IoTSensor).offset(skip).limit(limit))
    return result.scalars().all()

async def get_gis_data(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(GISData).offset(skip).limit(limit))
    return result.scalars().all()