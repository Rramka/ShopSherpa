"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "ShopSherpa"
    debug: bool = False
    environment: str = "development"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
