import os
from typing import Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    id: str = Field(..., description="The unique system-generated UUID assigned to the document.")
    filename: str = Field(..., description="The original name of the uploaded file.")
    storage_path: str = Field(..., description="The absolute local or cloud path where the file is stored.")
    file_size_bytes: int = Field(..., description="Size of the file on disk.")
    mime_type: str = Field(..., description="Determined MIME content type of the target asset.")
    
    @property
    def extension(self) -> str:
        """Helper property to extract the file extension cleanly."""
        _, ext = os.path.splitext(self.filename.lower())
        return ext
