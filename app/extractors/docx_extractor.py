import os
import docx

class DocxExtractor:
    @staticmethod
    async def extract(file_path: str) -> str:
        """Extracts textual paragraph structures from OpenXML Word files."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"DOCX target file not found: {file_path}")
            
        doc = docx.Document(file_path)
        # Combine all paragraphs with native line breaks
        text_content = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        
        return "\n".join(text_content)
