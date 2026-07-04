from pydantic import BaseModel, Field
from typing import Dict, Any

class Chunk(BaseModel):
    id: str = Field(..., description="The unique system-generated UUID identifying this isolated block.")
    parent_document_id: str = Field(..., description="The associated tracking identification code of the parent file.")
    text: str = Field(..., description="The text slice content of the chunk segment.")
    index: int = Field(..., description="The logical order sequence index tracking the position inside the original file.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom layout details like page numbers or author data.")

    def to_vector_metadata(self) -> Dict[str, Any]:
        """
        Flattens standard properties into a unified dictionary 
        safe for ingestion by relational or vector databases.
        """
        base = {
            "chunk_id": self.id,
            "document_id": self.parent_document_id,
            "chunk_index": self.index
        }
        # Merge tracking keys with any custom user metadata properties passed along
        return {**base, **self.metadata}
