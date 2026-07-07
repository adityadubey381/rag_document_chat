# RAG Document Chat

A full-stack document AI application that lets users upload PDF, DOCX, and TXT files, index them into a vector database, and chat with the content using retrieval-augmented generation (RAG).

## Features

- Upload and index documents
- Extract text from PDF, DOCX, and TXT files
- Chunk and embed document content
- Retrieve relevant context with semantic search
- Ask questions in natural language and get source-backed answers
- View and delete indexed documents
- Modern web interface for chatting with documents

## Tech Stack

- Backend: Python, FastAPI
- Frontend: HTML, CSS, JavaScript
- AI: OpenAI embeddings and chat models
- Vector DB: ChromaDB
- Storage: Local file system for uploaded documents and persistent vector data

## Project Structure

- app/ - FastAPI backend and services
- frontend/ - Web UI
- uploaded_files/ - Uploaded document storage
- vector_db/ - ChromaDB persistence
- docs/ - Project documentation

## Getting Started

1. Create and activate a virtual environment
2. Install dependencies
3. Set your OpenAI API key in a .env file
4. Run the app

Example:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install fastapi uvicorn openai chromadb pydantic-settings python-multipart
```

Create a .env file:

```env
OPENAI_API_KEY=your_openai_key_here
```

Run the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open http://127.0.0.1:8000

## Notes

- The app currently uses local storage for uploaded files and vector data.
- For production, make sure to use persistent storage and secure environment variables.

## License

This project is for demonstration and development purposes.
