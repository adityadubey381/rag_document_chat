import os

class TxtExtractor:
    @staticmethod
    async def extract(file_path: str) -> str:
        """Reads plain text files using standard UTF-8 fallback encodings."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TXT target file not found: {file_path}")
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback for systems writing text files in Windows-1252 or Latin-1
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
