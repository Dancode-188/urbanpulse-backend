from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.community import Project, Feedback
from app.api.schemas.community import ProjectCreate, FeedbackCreate

async def create_project(db: AsyncSession, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return result.scalars().all()

async def create_feedback(db: AsyncSession, feedback: FeedbackCreate, project_id: int, user_id: int):
    db_feedback = Feedback(**feedback.dict(), project_id=project_id, user_id=user_id)
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback