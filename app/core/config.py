"""
Centralized application configuration.
"""

from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    # === General ===
    APP_NAME: str = "RAG AI Backend"
    ENVIRONMENT: str = Field("development", description="Environment: dev/staging/prod")

    # === Google Gemini ===
    GEMINI_API_KEY: str = Field(..., description="Google Generative AI API key")
    EMBEDDING_MODEL_NAME: str = Field(
        "models/text-embedding-004",
        description="Gemini embedding model (default: text-embedding-004)"
    )

    # === Qdrant Vector DB ===
    QDRANT_URL: str = Field("http://localhost:6333", description="Qdrant endpoint URL")
    QDRANT_API_KEY: str | None = Field(None, description="Optional Qdrant API key")

    # === CORS / Frontend ===
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
