from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services import community_service
from app.api.schemas.community import Project, ProjectCreate, Feedback, FeedbackCreate

router = APIRouter()

@router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await community_service.create_project(db, project)

@router.get("/projects", response_model=List[Project])
async def read_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    projects = await community_service.get_projects(db, skip=skip, limit=limit)
    return projects

@router.post("/projects/{project_id}/feedback", response_model=Feedback)
async def create_feedback(project_id: int, feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Implement user authentication and get the user_id
    user_id = 1  # Placeholder
    return await community_service.create_feedback(db, feedback, project_id, user_id)