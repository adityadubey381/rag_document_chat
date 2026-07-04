import os
from fastapi import HTTPException
from app.extractors.pdf_extractor import PDFExtractor
from app.extractors.docx_extractor import DocxExtractor
from app.extractors.txt_extractor import TxtExtractor

class ExtractionService:
    def __init__(self):
        # Map file extensions to their respective extraction components
        self._extractors = {
            ".pdf": PDFExtractor,
            ".docx": DocxExtractor,
            ".txt": TxtExtractor
        }

    async def extract_text(self, file_path: str) -> str:
        """
        Detects the file format, extracts raw text content, 
        and validates that the output is not empty.
        """
        _, extension = os.path.splitext(file_path.lower())
        
        # 1. Match extension against supported extractors
        extractor = self._extractors.get(extension)
        if not extractor:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format '{extension}'. Supported formats: PDF, DOCX, TXT."
            )
            
        try:
            # 2. Execute target extraction asynchronously
            extracted_text = await extractor.extract(file_path)
            
            # 3. Handle edge cases where files contain only non-parseable images
            if not extracted_text or not extracted_text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="Extraction failed. The file is empty or contains non-extractable elements (like scanned images)."
                )
                
            return extracted_text.strip()
            
        except HTTPException as he:
            # Re-raise explicit HTTP exceptions
            raise he
        except Exception as e:
            # Shield raw server errors and provide structured log tracing strings
            raise HTTPException(
                status_code=500,
                detail=f"Internal extraction processing failure: {str(e)}"
            )
