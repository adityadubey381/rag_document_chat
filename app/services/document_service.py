from app.services.embedding_service import EmbeddingService
from app.vectorstore.chroma import ChromaStore

class DocumentService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaStore()

    async def ingest_chunks(self, chunks: list, metadatas: list, ids: list):
        # 1. Isolate text
        texts = [chunk for chunk in chunks]
        
        # 2. Vectorize text safely
        embeddings = await self.embedding_service.get_embeddings(texts)
        
        # 3. Save directly to your collection
        await self.vector_store.add_documents(texts, metadatas, ids)