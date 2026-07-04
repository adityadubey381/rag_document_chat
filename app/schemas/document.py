from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentMetadata(BaseModel):
    document_id: str = Field(..., description="The unique system-generated UUID for the document.")
    filename: str = Field(..., description="The sanitized base name of the uploaded file.")
    file_type: str = Field(..., description="The file extension format, e.g., '.pdf', '.txt'.")
    total_chunks: int = Field(..., description="The absolute count of text segments generated from the document.")

class DocumentResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the document operation was executed cleanly.")
    data: DocumentMetadata = Field(..., description="The main document metadata details.")

class DocumentDeleteResponse(BaseModel):
    document_id: str = Field(..., description="The UUID of the purge target.")
    success: bool = Field(True, description="Confirmation that the text and vector stores were wiped clean.")
    message: str = Field(default="Document indexes successfully cleared from system memory.")
