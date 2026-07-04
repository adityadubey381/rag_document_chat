from typing import List
from openai import AsyncOpenAI
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        """Only initialize what is needed to generate embeddings."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Fetches embeddings for a list of texts using OpenAI's API."""
        if not texts:
            return []
            
        # Clean text strings slightly by removing problematic line breaks
        cleaned_texts = [text.replace("\n", " ") for text in texts]
        
        response = await self.client.embeddings.create(
            model=self.model,
            input=cleaned_texts
        )
        
        # Sort by index to guarantee embeddings map 1:1 with input order
        sorted_data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in sorted_data]
