"""
Qdrant Vector Store integration using LangChain + Gemini Embeddings.
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from app.core.config import settings


def get_qdrant_client() -> QdrantClient:
    """
    Initialize and return a Qdrant client instance.
    Configuration values are loaded from environment via settings.
    """
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )


def get_vectorstore(collection_name: str) -> Qdrant:
    """
    Create or get a LangChain-compatible Qdrant vector store
    using Gemini embeddings.
    """
    # Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL_NAME,
        google_api_key=settings.GEMINI_API_KEY,
    )

    # Initialize Qdrant client
    client = get_qdrant_client()

    # Connect LangChain vectorstore
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    return vectorstore
