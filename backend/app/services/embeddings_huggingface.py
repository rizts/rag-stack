from huggingface_hub import InferenceClient
from app.core.config import settings
from typing import List


class HuggingFaceEmbeddingService:
    """
    This service provides text embeddings using HuggingFace Inference API.
    It is designed to be a drop-in replacement for other embedding providers.
    """

    def __init__(self):
        api_key = settings.HF_API_KEY
        if not api_key:
            raise ValueError("Missing HF_API_KEY environment variable.")
        
        self.client = InferenceClient(
            model=settings.EMBEDDING_MODEL_NAME,
            token=api_key
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text input.
        """
        response = self.client.feature_extraction(text)
        # Convert to list if it's not already
        if hasattr(response, 'tolist'):
            return response.tolist()
        return list(response)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple text inputs.
        """
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)
        return embeddings