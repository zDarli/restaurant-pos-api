from fastapi import FastAPI
from app.api.routers import health
from app.core.config import get_settings
from app.core.database import engine

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.include_router(health.router)
