from typing import List, Dict, Any
from app.vectorstore.chroma import ChromaStore

class RetrievalService:
    def __init__(self):
        self.vector_store = ChromaStore()

    async def retrieve_context(self, query: str, limit: int = 4, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Searches the underlying vector space and isolates relevant context snippets.
        
        Args:
            query: Natural language search string or chat question.
            limit: Total maximum context pieces to fetch (top_k).
            min_score: Relevance filter threshold (useful if using cosine distance).
        """
        if not query or not query.strip():
            return []

        # 1. Direct query lookup inside vector workspace
        raw_results = await self.vector_store.similarity_search(query=query, k=limit)
        
        filtered_results = []
        for item in raw_results:
            # Note: ChromaDB calculates distances (where lower distance = higher similarity)
            # If tracking similarity scores explicitly, convert or filter based on your vector settings
            filtered_results.append({
                "text": item["text"],
                "metadata": item["metadata"],
                "score": item.get("distance", 0.0)
            })

        return filtered_results

    async def get_formatted_context_string(self, query: str, limit: int = 4) -> str:
        """
        Fetches matching contexts and joins them into a unified context block 
        designed for direct insertion into LLM System Prompts.
        """
        contexts = await self.retrieve_context(query=query, limit=limit)
        
        if not contexts:
            return "No matching source document context found in the database."

        formatted_blocks = []
        for idx, ctx in enumerate(contexts):
            source_info = ctx['metadata'].get('filename', 'Unknown Source')
            chunk_idx = ctx['metadata'].get('chunk_index', 'N/A')
            
            block = f"[Source Document #{idx+1}: {source_info} (Section ID: {chunk_idx})]\n{ctx['text']}"
            formatted_blocks.append(block)

        return "\n\n--- EXTRACTED CONTEXT BOUNDARY ---\n\n".join(formatted_blocks)
