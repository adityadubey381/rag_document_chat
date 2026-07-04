from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload", status_code=200)
async def upload_file(file: UploadFile = File(...)):
    """Uploads a file to the API service."""
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF, DOCX, or TXT file.")
    
    # Here you would typically process the uploaded file, e.g., save it or analyze it.    
    return {"filename": file.filename, "content_type": file.content_type}