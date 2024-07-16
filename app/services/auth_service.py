from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.user import User
from app.core.security import verify_password, get_password_hash
from app.api.schemas.user import UserCreate

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user