from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from app.api.models.user import Base

class SpatialEntity(Base):
    __tablename__ = "spatial_entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    geometry = Column(Geometry(geometry_type='GEOMETRY', srid=4326))

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    geometry = Column(Geometry(geometry_type='POINT', srid=4326))

class Polygon(Base):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    geometry = Column(Geometry(geometry_type='POLYGON', srid=4326))