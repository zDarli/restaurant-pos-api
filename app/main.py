from fastapi import FastAPI
from app.api.routers import health

app = FastAPI(title="Restaurant POS API")

app.include_router(health.router)