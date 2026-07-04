from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorStore(ABC):
    @abstractmethod
    async def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        """Insert embedded chunks into the database."""
        pass

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """Retrieve most similar context chunks for a query."""
        pass