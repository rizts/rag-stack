from fastapi import APIRouter
from app.services.semantic import SemanticSearchService

router = APIRouter()

@router.post("/query")
def rag_query(query: str):
    """Receive a user query and return a simulated RAG response."""
    result = SemanticSearchService().search(query)
    return {"query": query, "result": result}
