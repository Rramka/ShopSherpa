"""Main FastAPI application."""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="ShopSherpa MVP - AI product chooser for headphones",
    version="0.1.0",
    debug=settings.debug,
)

# Include routers
app.include_router(health_router)
