import os
import google.generativeai as genai

class GeminiEmbeddingService:
    """
    This service provides text embeddings using Google's Gemini API.
    It is designed to be a drop-in replacement for other embedding providers.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)
        self.model = "models/embedding-001"

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text input.
        """
        result = genai.embed_content(model=self.model, content=text)
        return result["embedding"]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple text inputs.
        """
        embeddings = []
        for t in texts:
            res = genai.embed_content(model=self.model, content=t)
            embeddings.append(res["embedding"])
        return embeddings
