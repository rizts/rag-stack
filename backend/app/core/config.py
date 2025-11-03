"""
Centralized application configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):
    # === General ===
    APP_NAME: str = "RAG AI Backend"
    APP_VERSION: str = "0.1.0"
    APP_PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = Field("development", description="Environment: dev/staging/prod")

    # === Google Gemini ===
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")

    # === HuggingFace (optional fallback for embeddings) ===
    HF_API_KEY: Optional[str] = Field(None, description="HuggingFace API key (optional)")
    EMBEDDING_MODEL_NAME: str = Field(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        description="HuggingFace embedding model (default: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)"
    )

    # === Chunking ===
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100

    # === Qdrant Vector DB ===
    QDRANT_URL: str = Field("http://localhost:6333", description="Qdrant endpoint URL")
    QDRANT_API_KEY: Optional[str] = Field(None, description="Optional Qdrant API key")

    # === CORS / Frontend ===
    CORS_ORIGINS: str = "http://localhost:5173,https://your-vercel-app.vercel.app"

    # === Railway ===
    RAILWAY_TOKEN: Optional[str] = Field(None, description="Railway Token")
    RAILWAY_PROJECT_ID: Optional[str] = Field(None, description="Railway Project ID")

    # === Vercel (optional for CI/CD doc) ===
    VERCEL_TOKEN: Optional[str] = Field(None, description="Vercel Token")
    VERCEL_ORG_ID: Optional[str] = Field(None, description="Vercel Organization ID")
    VERCEL_PROJECT_ID: Optional[str] = Field(None, description="Vercel Project ID")

    # === Model Config ===
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # Ignore unknown .env keys (avoids ValidationError)
        case_sensitive=False  # Allow lowercase or uppercase env names
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Split CORS_ORIGINS env into list automatically."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


# Global settings instance
settings = Settings()
