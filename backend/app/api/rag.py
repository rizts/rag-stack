from fastapi import APIRouter, Form
from app.services.semantic import SemanticSearchService

router = APIRouter()
rag_service = SemanticSearchService()


@router.post("/index")
def index_document(content: str = Form(...)):
    """
    Receive raw text input, chunk it, embed with Gemini, and store in Qdrant.
    """
    result = rag_service.index_text(content)
    return {"status": "indexed", "detail": result}


@router.post("/query")
def rag_query(query: str = Form(...)):
    """
    Perform full RAG process:
    - Retrieve similar content from Qdrant
    - Generate a final answer using Gemini generative model
    """
    result = rag_service.generate_answer(query)
    return result
