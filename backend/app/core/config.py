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

    # === Embedding Provider Configuration ===
    EMBEDDING_PROVIDER: str = Field(
        "jina",
        description="Embedding provider: 'jina', 'cohere', 'voyage', or 'huggingface'"
    )
    
    # === Jina AI (Recommended for free tier) ===
    JINA_API_KEY: Optional[str] = Field(None, description="Jina AI API key")
    JINA_MODEL_NAME: str = Field(
        "jina-embeddings-v3",
        description="Jina embedding model (jina-embeddings-v3 or jina-embeddings-v2-base-en)"
    )
    
    # === HuggingFace (Legacy - not recommended for free tier) ===
    HF_API_KEY: Optional[str] = Field(None, description="HuggingFace API key")
    EMBEDDING_MODEL_NAME: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2",
        description="HuggingFace embedding model (only if using HF provider)"
    )
    
    # === Cohere (Alternative) ===
    COHERE_API_KEY: Optional[str] = Field(None, description="Cohere API key")
    
    # === Voyage AI (Alternative) ===
    VOYAGE_API_KEY: Optional[str] = Field(None, description="Voyage AI API key")

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
        extra="ignore",
        case_sensitive=False
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Split CORS_ORIGINS env into list automatically."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def embedding_dimension(self) -> int:
        """Return embedding dimension based on provider and model."""
        if self.EMBEDDING_PROVIDER == "jina":
            if "v3" in self.JINA_MODEL_NAME:
                return 1024  # jina-embeddings-v3
            else:
                return 768   # jina-embeddings-v2
        elif self.EMBEDDING_PROVIDER == "cohere":
            return 1024
        elif self.EMBEDDING_PROVIDER == "voyage":
            return 1024
        elif self.EMBEDDING_PROVIDER == "huggingface":
            return 384  # Default for sentence-transformers
        else:
            return 768  # Safe default


# Global settings instance
settings = Settings()