from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    """Simple health check endpoint for uptime monitoring."""
    return {"status": "ok"}
