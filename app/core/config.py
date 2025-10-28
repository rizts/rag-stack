from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application configuration using environment variables."""
    ENV: str = "dev"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
