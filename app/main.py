"""Main FastAPI application module."""

from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="ShopSherpa",
    description="ShopSherpa FastAPI service",
    version="0.1.0",
)

app.include_router(health_router)
