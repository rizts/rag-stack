"""
Unified embedding service supporting multiple providers.
Supports: Jina AI, Cohere, Voyage AI, and HuggingFace
"""

import requests
from typing import List
from app.core.config import settings


class EmbeddingService:
    """
    Unified embedding service that supports multiple providers.
    Provider is selected via EMBEDDING_PROVIDER in config.
    """

    def __init__(self):
        self.provider = settings.EMBEDDING_PROVIDER.lower()
        
        # Initialize provider-specific client
        if self.provider == "jina":
            self._init_jina()
        elif self.provider == "cohere":
            self._init_cohere()
        elif self.provider == "voyage":
            self._init_voyage()
        elif self.provider == "huggingface":
            self._init_huggingface()
        else:
            raise ValueError(
                f"Unsupported embedding provider: {self.provider}. "
                f"Supported: 'jina', 'cohere', 'voyage', 'huggingface'"
            )

    def _init_jina(self):
        """Initialize Jina AI embeddings."""
        if not settings.JINA_API_KEY:
            raise ValueError("JINA_API_KEY is required when using Jina provider")
        
        self.api_key = settings.JINA_API_KEY
        self.model = settings.JINA_MODEL_NAME
        self.api_url = "https://api.jina.ai/v1/embeddings"
        
        print(f"✅ Jina AI Embeddings initialized with model: {self.model}")

    def _init_cohere(self):
        """Initialize Cohere embeddings."""
        if not settings.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is required when using Cohere provider")
        
        try:
            import cohere
            self.client = cohere.Client(settings.COHERE_API_KEY)
            self.model = "embed-multilingual-v3.0"
            print(f"✅ Cohere Embeddings initialized")
        except ImportError:
            raise ImportError("Please install cohere: pip install cohere")

    def _init_voyage(self):
        """Initialize Voyage AI embeddings."""
        if not settings.VOYAGE_API_KEY:
            raise ValueError("VOYAGE_API_KEY is required when using Voyage provider")
        
        try:
            import voyageai
            self.client = voyageai.Client(api_key=settings.VOYAGE_API_KEY)
            self.model = "voyage-multilingual-2"
            print(f"✅ Voyage AI Embeddings initialized")
        except ImportError:
            raise ImportError("Please install voyageai: pip install voyageai")

    def _init_huggingface(self):
        """Initialize HuggingFace embeddings (legacy)."""
        if not settings.HF_API_KEY:
            raise ValueError("HF_API_KEY is required when using HuggingFace provider")
        
        try:
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(
                model=settings.EMBEDDING_MODEL_NAME,
                token=settings.HF_API_KEY
            )
            self.model = settings.EMBEDDING_MODEL_NAME
            print(f"⚠️  HuggingFace Embeddings initialized (not recommended for production)")
        except ImportError:
            raise ImportError("Please install huggingface-hub: pip install huggingface-hub")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        if self.provider == "jina":
            return self._embed_jina([text])[0]
        elif self.provider == "cohere":
            return self._embed_cohere([text])[0]
        elif self.provider == "voyage":
            return self._embed_voyage([text])[0]
        elif self.provider == "huggingface":
            return self._embed_huggingface_single(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing).
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
        """
        if self.provider == "jina":
            return self._embed_jina(texts)
        elif self.provider == "cohere":
            return self._embed_cohere(texts)
        elif self.provider == "voyage":
            return self._embed_voyage(texts)
        elif self.provider == "huggingface":
            return [self._embed_huggingface_single(text) for text in texts]

    def _embed_jina(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using Jina AI API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "input": texts,
            "encoding_type": "float"
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            embeddings = [item["embedding"] for item in result["data"]]
            return embeddings
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RuntimeError(
                    "Authentication error with Jina AI. Please verify your JINA_API_KEY is correct."
                )
            elif e.response.status_code == 429:
                raise RuntimeError(
                    "Rate limit exceeded for Jina AI. Please wait before making more requests."
                )
            else:
                raise RuntimeError(f"Jina AI API error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error calling Jina AI: {str(e)}")

    def _embed_cohere(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using Cohere API."""
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            raise RuntimeError(f"Cohere API error: {str(e)}")

    def _embed_voyage(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using Voyage AI API."""
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model
            )
            return response.embeddings
        except Exception as e:
            raise RuntimeError(f"Voyage AI API error: {str(e)}")

    def _embed_huggingface_single(self, text: str) -> List[float]:
        """Embed single text using HuggingFace Inference API."""
        try:
            import numpy as np
            response = self.client.feature_extraction(text)
            
            if isinstance(response, np.ndarray):
                return response.flatten().tolist()
            elif isinstance(response, list):
                return [float(x) for x in response]
            else:
                return list(response)
                
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "Not Found" in error_msg:
                raise RuntimeError(
                    f"Model {self.model} not available via HuggingFace Inference API. "
                    f"Consider switching to Jina AI for better reliability. "
                    f"Set EMBEDDING_PROVIDER=jina in your .env file."
                )
            elif "401" in error_msg:
                raise RuntimeError(
                    "Authentication error with HuggingFace API. Please verify your HF_API_KEY."
                )
            else:
                raise RuntimeError(f"HuggingFace API error: {error_msg}")


EmbeddingService = EmbeddingService