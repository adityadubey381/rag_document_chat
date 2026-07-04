from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.chat_service import ChatService

router = APIRouter()

class ChatQueryRequest(BaseModel):
    message: str
    top_k: int = 4

class ChatQueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

@router.post("/query", response_model=ChatQueryResponse)
async def query_documents(payload: ChatQueryRequest, chat_service: ChatService = Depends()):
    """
    Submits a natural language query over your uploaded vector dataset.
    Performs vector extraction and feeds relevant details to the configured LLM.
    """
    try:
        result = await chat_service.execute_rag_flow(
            user_query=payload.message, 
            limit=payload.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG processing failed: {str(e)}")