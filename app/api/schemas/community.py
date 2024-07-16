from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FeedbackBase(BaseModel):
    content: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    project_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    feedbacks: List[Feedback] = []

    class Config:
        orm_mode = True