from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.api.errors import NotFoundException, BadRequestException, ConflictException
from app.utils.common import validate_email

async def create_user(db: AsyncSession, user: UserCreate):
    if not validate_email(user.email):
        raise BadRequestException("Invalid email format")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=False
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Username or email already registered")
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundException("User not found")
    return user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user(db, user_id)
    update_data = user_update.dict(exclude_unset=True)

    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    await db.delete(user)
    await db.commit()
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user