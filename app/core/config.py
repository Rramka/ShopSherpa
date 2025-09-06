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

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
