from app.vectorstore.chroma import ChromaStore
from app.services.llm_service import LLMService

class ChatService:
    def __init__(self):
        self.vector_store = ChromaStore()
        self.llm_service = LLMService()

    async def execute_rag_flow(self, user_query: str, limit: int = 4) -> dict:
        """Performs full context-retrieval loop before querying the LLM."""
        # 1. Fetch matching context windows
        matched_chunks = await self.vector_store.similarity_search(user_query, k=limit)
        
        # 2. Extract and format context
        context_str = "\n\n--- NEXT CHUNK ---\n\n".join([c["text"] for c in matched_chunks])
        
        # 3. Create context-aware query structure
        rag_prompt = f"""Use the following pieces of context to answer the question at the end. 
If you do not know the answer based on the context, say that you don't know. Do not make things up.

CONTEXT:
{context_str}

QUESTION:
{user_query}
"""
        
        # 4. Synthesize final answer via LLM
        system_instruction = "You are an AI document assistant. Answer user prompts using only provided contexts."
        answer = await self.llm_service.generate_response(rag_prompt, system_instruction)
        
        return {
            "answer": answer,
            "sources": [c["metadata"] for c in matched_chunks]
        }

