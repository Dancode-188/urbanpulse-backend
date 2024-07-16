# app/main.py
from fastapi import FastAPI
from app.api.endpoints import auth, users, data, community
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Include the routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(data.router, prefix="/data", tags=["Data"])
app.include_router(community.router, prefix="/community", tags=["Community"])

@app.get("/")
def read_root():
    return {"message": "Welcome to UrbanPulse Backend API"}
