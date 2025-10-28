from typing import Dict, Optional, List
from app.utils.chunking import chunk_text
from app.services.embeddings_gemini import GeminiEmbeddingService
from app.services.vectorstore_qdrant import QdrantClientWrapper, Document

class SemanticSearchService:
    """
    Implements a RAG (Retrieval-Augmented Generation) pipeline
    using Gemini embeddings and Qdrant vector database.
    """

    def __init__(self):
        self.embeddings = GeminiEmbeddingService()
        self.collection = "documents"
        self.qdrant = QdrantClientWrapper(collection_name=self.collection)

    def index_text(self, text: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Split a large document into chunks, embed each chunk, and store in Qdrant.
        """
        chunks = chunk_text(text)
        documents: List[Document] = [
            Document(page_content=chunk, metadata=(metadata or {})) for chunk in chunks
        ]
        self.qdrant.add_documents(documents, embeddings=self.embeddings)
        return {"chunks_indexed": len(chunks)}

    def search(self, query: str, top_k: int = 3) -> Dict:
        """
        Perform semantic search using Gemini embeddings.
        Returns top-k most similar text chunks from Qdrant with scores.
        """
        results: List[Document] = self.qdrant.similarity_search(query, embeddings=self.embeddings, k=top_k)
        return {
            "query": query,
            "matches": [
                {
                    "score": r.score,
                    "content": r.page_content,
                    **r.metadata
                } for r in results
            ]
        }
