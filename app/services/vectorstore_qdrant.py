"""
Qdrant Vector Store integration using Gemini Embeddings.
Fully compatible with LangChain 1.0.2 (no deprecated imports).
"""

from typing import Any, Dict, List
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from app.core.config import settings

# Minimal Document class to replace LangChain Document
class Document:
    """
    Simple document structure to hold content and metadata.
    """
    def __init__(self, page_content: str, metadata: Dict[str, Any] = None):
        self.page_content = page_content
        self.metadata = metadata or {}

class QdrantClientWrapper:
    """
    Wrapper around QdrantClient to provide a simple add/search interface
    compatible with previous LangChain Qdrant usage.
    """

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

        # Ensure collection exists
        try:
            self.client.get_collection(collection_name=collection_name)
        except Exception:
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,  # embedding dimension
                    distance=Distance.COSINE
                )
            )

    def add_documents(self, documents: List[Document], embeddings: Any = None):
        """
        Add a list of Document objects with embeddings to Qdrant.
        If embeddings object is provided, use it; otherwise assume vectors are precomputed.
        """
        vectors = [embeddings.embed_text(doc.page_content) for doc in documents] if embeddings else []
        points = [
            {"id": str(i), "vector": vec, "payload": {"content": doc.page_content, **doc.metadata}}
            for i, (doc, vec) in enumerate(zip(documents, vectors))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def similarity_search(self, query: str, embeddings: Any, k: int = 5) -> List[Document]:
        """
        Search for top-k most similar documents using embeddings.
        """
        query_vector = embeddings.embed_text(query)
        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k
        )
        return [Document(page_content=p.payload.get("content", ""), metadata=p.payload) for p in response]
