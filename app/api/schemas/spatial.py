from pydantic import BaseModel
from typing import List, Optional
from geojson_pydantic import Point, Polygon, Feature, FeatureCollection

class SpatialEntityBase(BaseModel):
    name: str
    type: str

class SpatialEntityCreate(SpatialEntityBase):
    geometry: Feature

class SpatialEntity(SpatialEntityBase):
    id: int
    geometry: Feature

    class Config:
        orm_mode = True

class PointBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int
    geometry: Point

    class Config:
        orm_mode = True

class PolygonBase(BaseModel):
    name: str

class PolygonCreate(PolygonBase):
    geometry: Polygon

class Polygon(PolygonBase):
    id: int
    geometry: Polygon

    class Config:
        orm_mode = True