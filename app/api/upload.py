from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.upload_service import UploadService

router = APIRouter()

@router.post("/upload", status_code=200)
async def upload_file(file: UploadFile = File(...), upload_service: UploadService = Depends()):
    """Uploads a file to the API service and indexes it in the vector DB."""
    if not file.filename or not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF, DOCX, or TXT file.")
    
    return await upload_service.process_and_index_file(file)