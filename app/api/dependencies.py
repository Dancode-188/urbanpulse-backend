from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.services import user_service
from app.api.errors import UnauthorizedException
from app.api.schemas.user import TokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException("Could not validate credentials")
        token_data = TokenData(username=username)
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")

    user = await user_service.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise UnauthorizedException("User not found")
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_pagination_params(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}