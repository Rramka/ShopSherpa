"""Application configuration using pydantic-settings."""

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = Field(default="ShopSherpa", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")
    database_url: str = Field(
        default="postgresql://user:password@localhost/shopsherpa",
        description="Database connection URL"
    )
    
    # Celery settings
    celery_broker_url: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL"
    )
    celery_task_serializer: str = Field(default="json", description="Task serializer")
    celery_result_serializer: str = Field(default="json", description="Result serializer")
    celery_accept_content: list[str] = Field(default=["json"], description="Accepted content types")
    celery_timezone: str = Field(default="UTC", description="Celery timezone")
    celery_enable_utc: bool = Field(default=True, description="Enable UTC")

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
