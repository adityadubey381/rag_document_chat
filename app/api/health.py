from fastapi import APIRouter

router = APIRouter()

@router.get("/health", status_code=200)
async def health_check():
    """Verifies that the API service is active and responsive."""
    return {"status": "healthy", "service": "document-ai-api"}

