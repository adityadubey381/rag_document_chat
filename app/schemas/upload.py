from pydantic import BaseModel, Field

class UploadSuccessDetails(BaseModel):
    document_id: str = Field(..., description="The newly minted unique tracking identification string.")
    filename: str = Field(..., description="The final safely resolved name of the processed file.")
    total_chunks: int = Field(..., description="The exact count of text pieces committed to the vector database.")
    status: str = Field(default="successfully_indexed", description="The current execution status of the asset workflow.")

class UploadResponse(BaseModel):
    success: bool = Field(default=True, description="Confirms that the asset was completely digested without runtime failures.")
    details: UploadSuccessDetails = Field(..., description="Metadata payload containing system tracking metrics.")
