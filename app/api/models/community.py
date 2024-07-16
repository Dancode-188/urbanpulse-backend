from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.api.models.user import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    feedbacks = relationship("Feedback", back_populates="project")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")