"""
Centralized application configuration.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # === General ===
    APP_NAME: str = "RAG AI Backend"
    ENVIRONMENT: str = Field("development", description="Environment: dev/staging/prod")

    # === Google Gemini ===
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")

    # === HuggingFace ===
    HF_API_KEY: str = Field(..., description="HuggingFace AI API key")
    EMBEDDING_MODEL_NAME: str = Field(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        description="HuggingFace embedding model (default: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)"
    )

    # === Qdrant Vector DB ===
    QDRANT_URL: str = Field("http://localhost:6333", description="Qdrant endpoint URL")
    QDRANT_API_KEY: str | None = Field(None, description="Optional Qdrant API key")

    # === CORS / Frontend ===
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Split CORS_ORIGINS env into a list automatically."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
