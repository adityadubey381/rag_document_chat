import os
from pypdf import PdfReader

class PDFExtractor:
    @staticmethod
    async def extract(file_path: str) -> str:
        """Extracts and normalizes raw text from all pages of a PDF file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF target file not found: {file_path}")
            
        text_content = []
        reader = PdfReader(file_path)
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
                
        return "\n".join(text_content)
