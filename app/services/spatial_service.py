from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.spatial import SpatialEntity, Point, Polygon
from app.api.schemas.spatial import SpatialEntityCreate, PointCreate, PolygonCreate
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

async def create_spatial_entity(db: AsyncSession, entity: SpatialEntityCreate):
    geom = shape(entity.geometry.geometry)
    db_entity = SpatialEntity(
        name=entity.name,
        type=entity.type,
        geometry=from_shape(geom, srid=4326)
    )
    db.add(db_entity)
    await db.commit()
    await db.refresh(db_entity)
    return db_entity

async def create_point(db: AsyncSession, point: PointCreate):
    db_point = Point(
        name=point.name,
        latitude=point.latitude,
        longitude=point.longitude,
        geometry=f'POINT({point.longitude} {point.latitude})'
    )
    db.add(db_point)
    await db.commit()
    await db.refresh(db_point)
    return db_point

async def create_polygon(db: AsyncSession, polygon: PolygonCreate):
    geom = shape(polygon.geometry)
    db_polygon = Polygon(
        name=polygon.name,
        geometry=from_shape(geom, srid=4326)
    )
    db.add(db_polygon)
    await db.commit()
    await db.refresh(db_polygon)
    return db_polygon

async def get_spatial_entities(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(SpatialEntity).offset(skip).limit(limit))
    return result.scalars().all()

async def get_points(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Point).offset(skip).limit(limit))
    return result.scalars().all()

async def get_polygons(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Polygon).offset(skip).limit(limit))
    return result.scalars().all()