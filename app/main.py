from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os

# Add parent directory to path so 'app' module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.documents import router as documents_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise ready production architecture for text vector indexing and document conversational interfaces."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wire unified routing system
app.include_router(health_router, prefix=settings.API_V1_STR, tags=["Diagnostics"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["AI Engine"])
app.include_router(upload_router, prefix=settings.API_V1_STR, tags=["Upload Engine"])
app.include_router(documents_router, prefix=f"{settings.API_V1_STR}/documents", tags=["Document Management"])

# Ensure frontend directory exists before mounting
os.makedirs("frontend", exist_ok=True)

# Mount static files to serve the frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
