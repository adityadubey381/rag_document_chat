import chromadb
from typing import List, Dict, Any
from app.vectorstore.base import BaseVectorStore
from app.core.config import settings
from app.services.embedding_service import EmbeddingService

class ChromaStore(BaseVectorStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_DIR)
        self.embedding_service = EmbeddingService()
        self.collection = self.client.get_or_create_collection(
            name="rag_documents"
        )

    async def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        embeddings = await self.embedding_service.get_embeddings(texts)
        # Convert metadata to chromadb-compatible format (all values must be str, int, float, or bool)
        safe_metadatas = [{k: str(v) if v is not None else None for k, v in m.items()} for m in metadatas]
        self.collection.add(
            documents=texts,
            embeddings=embeddings,  # type: ignore
            metadatas=safe_metadatas,  # type: ignore
            ids=ids
        )

    async def similarity_search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        query_embedding = (await self.embedding_service.get_embeddings([query]))[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        formatted_results = []
        if results and results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0
                })
        return formatted_results

    async def delete_document(self, document_id: str) -> None:
        """Deletes all chunks associated with a document_id from ChromaDB."""
        self.collection.delete(where={"document_id": document_id})