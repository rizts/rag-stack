from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import setup_logger
from app.api import health, rag

# Initialize logger before app creation
setup_logger()

# Create FastAPI instance
app = FastAPI(title="RAG API", version="0.1.0")

# Allow frontend connection (Vercel or localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])

# Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "RAG API is running", "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.APP_PORT,
        reload=True,
    )
