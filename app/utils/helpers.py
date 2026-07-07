import os
from fastapi import HTTPException

# Define strict size thresholds (e.g., 25 MegaBytes)
MAX_FILE_SIZE = 25 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def validate_uploaded_file(filename: str, file_size: int) -> None:
    """Verifies that an incoming asset fits within system processing limits."""
    # 1. Enforce strict extension matching
    _, ext = os.path.splitext(filename.lower())
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Extension '{ext}' is not supported. Allowed types: PDF, DOCX, TXT."
        )

    # 2. Prevent server resource exhaustion attacks
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum permissible safety size limit of {MAX_FILE_SIZE // (1024 * 1024)}MB."
        )
