from fastapi import FastAPI
from app.core.config import settings
from app.api.chat import router as chat_router
from app.api.health import router as health_router  # Assuming base route file exists

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise ready production architecture for text vector indexing and document conversational interfaces."
)

# Wire unified routing system
app.include_router(health_router, prefix=settings.API_V1_STR, tags=["Diagnostics"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["AI Engine"])

@app.get("/")
def read_root():
    return {"status": "online", "docs": "/docs"}
