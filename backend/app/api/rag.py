import os
from fastapi import APIRouter, Form, UploadFile, File
from app.services.semantic import SemanticSearchService
from app.services.file_parser import FileParser
from app.utils.chunking import chunk_text

router = APIRouter()
rag_service = SemanticSearchService()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/index")
def index_document(content: str = Form(...)):
    """
    Receive raw text input, chunk it, embed with Gemini, and store in Qdrant.
    """
    result = rag_service.index_text(content)
    return {"status": "indexed", "detail": result}

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Accept a file upload (PDF or TXT), extract its content, and show chunk preview.
    Does not store embeddings yet — only returns processed chunks.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Detect type
    if file.filename.lower().endswith(".pdf"):
        text = FileParser.parse_pdf(file_path)
    elif file.filename.lower().endswith(".txt"):
        text = FileParser.parse_txt(file_path)
    else:
        return {"error": "Unsupported file format. Please upload .pdf or .txt"}

    chunks = chunk_text(text)
    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "sample_chunks": chunks[:5],  # limit preview
    }

@router.post("/query")
def rag_query(query: str = Form(...)):
    """
    Perform full RAG process:
    - Retrieve similar content from Qdrant
    - Generate a final answer using Gemini generative model
    """
    result = rag_service.generate_answer(query)
    return result
