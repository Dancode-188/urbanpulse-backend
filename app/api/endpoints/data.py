from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services import data_service, ai_interface_service, spatial_service
from app.api.schemas.data import IoTSensor, IoTSensorCreate, SensorReading, SensorReadingCreate, GISData, GISDataCreate
from app.api.schemas.spatial import SpatialEntity, SpatialEntityCreate, Point, PointCreate, Polygon, PolygonCreate
from app.api.schemas.user import User
from app.api.dependencies import get_current_active_user, get_pagination_params
from app.api.errors import NotFoundException, BadRequestException
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/iot-sensor", response_model=IoTSensor)
async def create_iot_sensor(
    sensor: IoTSensorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await data_service.create_iot_sensor(db, sensor)

@router.get("/iot-sensor", response_model=List[IoTSensor])
async def read_iot_sensors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    sensors = await data_service.get_iot_sensors(db, **pagination)
    return sensors

@router.post("/iot-sensors/{sensor_id}/readings", response_model=SensorReading)
async def create_sensor_reading(
    sensor_id: int,
    reading: SensorReadingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return await data_service.create_sensor_reading(db, reading, sensor_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/gis-data", response_model=GISData)
async def create_gis_data(
    gis_data: GISDataCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await data_service.create_gis_data(db, gis_data)

@router.get("/gis-data", response_model=List[GISData])
async def read_gis_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    gis_data = await data_service.get_gis_data(db, **pagination)
    return gis_data

@router.get("/predict/water-shortage")
async def request_water_shortage_prediction(
    lat: float,
    lon: float,
    days: int = 7,
    current_user: User = Depends(get_current_active_user)
):
    location = (lat, lon)
    time_range = (datetime.now(), datetime.now() + timedelta(days=days))
    return await ai_interface_service.request_water_shortage_prediction(location, time_range)

@router.get("/predict/noise-pollution")
async def request_noise_pollution_prediction(
    lat: float,
    lon: float,
    days: int = 7,
    current_user: User = Depends(get_current_active_user)
):
    location = (lat, lon)
    time_range = (datetime.now(), datetime.now() + timedelta(days=days))
    return await ai_interface_service.request_noise_pollution_prediction(location, time_range)

@router.get("/predict/flood-risk")
async def request_flood_risk_prediction(
    lat: float,
    lon: float,
    days: int = 7,
    current_user: User = Depends(get_current_active_user)
):
    location = (lat, lon)
    time_range = (datetime.now(), datetime.now() + timedelta(days=days))
    return await ai_interface_service.request_flood_risk_prediction(location, time_range)

@router.post("/spatial-entity", response_model=SpatialEntity)
async def create_spatial_entity(
    entity: SpatialEntityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await spatial_service.create_spatial_entity(db, entity)

@router.get("/spatial-entities", response_model=List[SpatialEntity])
async def read_spatial_entities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    entities = await spatial_service.get_spatial_entities(db, **pagination)
    return entities

@router.post("/point", response_model=Point)
async def create_point(
    point: PointCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await spatial_service.create_point(db, point)

@router.get("/points", response_model=List[Point])
async def read_points(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    points = await spatial_service.get_points(db, **pagination)
    return points

@router.post("/polygon", response_model=Polygon)
async def create_polygon(
    polygon: PolygonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await spatial_service.create_polygon(db, polygon)

@router.get("/polygons", response_model=List[Polygon])
async def read_polygons(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    polygons = await spatial_service.get_polygons(db, **pagination)
    return polygons