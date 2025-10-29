"""
Qdrant Vector Store integration using Gemini Embeddings.
Includes similarity scores.
"""

from typing import Any, Dict, List
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from app.core.config import settings
import uuid

# Minimal Document class
class Document:
    """
    Simple document structure to hold content, metadata, and optional score.
    """
    def __init__(self, page_content: str, metadata: Dict[str, Any] = None, score: float = None):
        self.page_content = page_content
        self.metadata = metadata or {}
        self.score = score

class QdrantClientWrapper:
    """
    Wrapper around QdrantClient to provide add/search interface with score support.
    """

    def __init__(self, collection_name: str, vector_size: int = 384):  # Default to 384 for HuggingFace embeddings
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            check_compatibility=False
        )

        # Recreate collection to ensure correct vector dimension
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,  # embedding dimension
                distance=Distance.COSINE
            )
        )

    def add_documents(self, documents: List[Document], embeddings: Any):
        """
        Add a list of Document objects with embeddings to Qdrant.
        """
        vectors = [embeddings.embed_text(doc.page_content) for doc in documents]
        points = [
            {"id": str(uuid.uuid4()), "vector": vec, "payload": {"content": doc.page_content, **doc.metadata}}
            for i, (doc, vec) in enumerate(zip(documents, vectors))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def upsert_vectors(self, collection_name: str, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        """
        Upsert vectors with payloads to the specified collection.
        """
        points = [
            {"id": str(uuid.uuid4()), "vector": vec, "payload": payload}
            for i, (vec, payload) in enumerate(zip(vectors, payloads))
        ]
        self.client.upsert(collection_name=collection_name, points=points)

    def search_vectors(self, collection_name: str, query_vector: List[float], top_k: int = 5):
        """
        Search for top-k most similar vectors in the collection.
        """
        response = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return response

    def similarity_search(self, query: str, embeddings: Any, k: int = 5) -> List[Document]:
        """
        Search for top-k most similar documents and include similarity score.
        """
        query_vector = embeddings.embed_text(query)
        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k
        )
        results = []
        for p in response:
            content = p.payload.get("content", "")
            score = 1 - p.score if p.score is not None else None  # Qdrant returns distance, convert to similarity
            results.append(Document(page_content=content, metadata=p.payload, score=score))
        return results
