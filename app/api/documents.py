import os
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.vectorstore.chroma import ChromaStore
from app.core.config import settings

router = APIRouter()

@router.get("", response_model=List[Dict[str, Any]])
async def list_documents(chroma_store: ChromaStore = Depends()):
    """
    Retrieves a list of all unique documents currently indexed in the vector store.
    """
    try:
        # Fetch all metadatas from the collection
        results = chroma_store.collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])
        
        # Deduplicate documents based on document_id
        unique_docs = {}
        for m in metadatas:
            if m and "document_id" in m:
                doc_id = m["document_id"]
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = {
                        "document_id": doc_id,
                        "filename": m.get("filename", "Unknown"),
                        "file_type": m.get("file_type", "")
                    }
        return list(unique_docs.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents list: {str(e)}")

@router.delete("/{document_id}", status_code=200)
async def delete_document(document_id: str, chroma_store: ChromaStore = Depends()):
    """
    Deletes all vectors and files associated with a given document_id.
    """
    try:
        # 1. Retrieve the file metadata to find the file extension on disk
        results = chroma_store.collection.get(
            where={"document_id": document_id}, 
            limit=1, 
            include=["metadatas"]
        )
        metadatas = results.get("metadatas", [])
        
        if not metadatas:
            raise HTTPException(status_code=404, detail="Document not found or already deleted.")
            
        file_type = metadatas[0].get("file_type", "")
        
        # 2. Delete from ChromaDB
        await chroma_store.delete_document(document_id)
        
        # 3. Delete physical file from upload directory
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document_id}{file_type}")
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {"status": "success", "message": f"Document {document_id} successfully deleted."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
