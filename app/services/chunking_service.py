from typing import List, Dict, Any

class ChunkingService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def split_text(self, text: str, metadata_template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Splits raw string content into structured overlapping chunks."""
        chunks = []
        words = text.split()
        
        # Simple step-based slider window processing
        step = self.chunk_size - self.chunk_overlap
        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            meta = metadata_template.copy()
            meta["chunk_index"] = len(chunks)
            meta["chunk_id"] = f"{metadata_template.get('document_id', 'doc')}_{meta['chunk_index']}"
            
            chunks.append({
                "text": chunk_text,
                "metadata": meta
            })
            if i + self.chunk_size >= len(words):
                break
                
        return chunks
