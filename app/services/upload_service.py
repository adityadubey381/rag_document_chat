import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.services.extraction_service import ExtractionService
from app.services.cleaning_service import CleaningService
from app.services.chunking_service import ChunkingService
from app.vectorstore.chroma import ChromaStore

class UploadService:
    def __init__(self):
        self.extraction_service = ExtractionService()
        self.cleaning_service = CleaningService()
        self.chunking_service = ChunkingService()
        self.vector_store = ChromaStore()

    async def process_and_index_file(self, file: UploadFile) -> dict:
        """
        Orchestrates the entire data ingestion pipeline:
        Saves file -> Extracts text -> Cleans text -> Chunks text -> Generates Vector Index.
        """
        # 1. Generate unique file IDs and sanitize paths
        document_id = str(uuid.uuid4())
        safe_filename = os.path.basename(file.filename)
        _, extension = os.path.splitext(safe_filename.lower())
        
        target_file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}{extension}")

        try:
            # 2. Persist uploaded file bytes to disk safely
            with open(target_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 3. Core Text Processing Pipeline
            raw_text = await self.extraction_service.extract_text(target_file_path)
            clean_text = await self.cleaning_service.clean_text(raw_text)
            
            # Base metadata to propagate down to every single sub-chunk for traceability
            base_metadata = {
                "document_id": document_id,
                "filename": safe_filename,
                "file_type": extension
            }
            
            chunks = await self.chunking_service.create_chunks(clean_text, base_metadata)
            
            if not chunks:
                raise HTTPException(status_code=422, detail="No extractable or indexable content found.")

            # 4. Prepare data arrays for vector engine ingestion
            texts = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]
            ids = [c["metadata"]["chunk_id"] for c in chunks]

            # 5. Commit structured text vectors to the database
            await self.vector_store.add_documents(texts=texts, metadatas=metadatas, ids=ids)

            return {
                "document_id": document_id,
                "filename": safe_filename,
                "total_chunks": len(chunks),
                "status": "successfully_indexed"
            }

        except Exception as e:
            # Clean up the orphan file from disk if processing crashes midway
            if os.path.exists(target_file_path):
                os.remove(target_file_path)
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"File indexing pipeline aborted: {str(e)}")
