from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token
from app.core.database import get_db
from app.services.auth_service import authenticate_user, create_user
from app.api.schemas.user import User, UserCreate, Token
from app.api.errors import UnauthorizedException

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    return db_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException("Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}