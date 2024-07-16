from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services import user_service
from app.api.schemas.user import User, UserCreate, UserUpdate
from app.api.dependencies import get_current_active_user, get_current_superuser, get_pagination_params

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    return await user_service.create_user(db, user)

@router.get("/", response_model=List[User])
async def read_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    pagination: dict = Depends(get_pagination_params)
):
    users = await user_service.get_users(db, **pagination)
    return users

@router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_user = await user_service.get_user(db, user_id)
    return db_user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    updated_user = await user_service.update_user(db, user_id, user_update)
    return updated_user

@router.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    deleted_user = await user_service.delete_user(db, user_id)
    return deleted_user