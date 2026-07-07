# RAG Document Chat Project Documentation

## 1. Overview

RAG Document Chat is a full-stack document intelligence application that lets users upload documents, index them into a vector database, and ask questions in natural language. The system uses retrieval-augmented generation (RAG) to ground answers in the uploaded content instead of relying only on the model’s general knowledge.

The project combines a Python backend, a lightweight frontend, and an AI-powered retrieval pipeline to provide a conversational document assistant experience.

---

## 2. Purpose of the Project

This application is designed to help users:

- Upload PDF, DOCX, and TXT documents
- Extract and clean text content from those files
- Split the content into searchable chunks
- Store the chunks in a vector database
- Ask questions about the documents and receive source-backed answers
- Delete indexed documents when they are no longer needed

It is useful for research documents, technical manuals, reports, books, and other text-heavy materials.

---

## 3. Technology Stack

### Backend
- Python
- FastAPI for API development
- Pydantic and Pydantic Settings for data validation and configuration
- Uvicorn for running the server

### Frontend
- Plain HTML, CSS, and JavaScript
- No heavy framework is required for this version
- Fetch API for communicating with the backend

### AI and Embeddings
- OpenAI API for embeddings and chat completions
- GPT-based language model for answer generation
- Embedding model for semantic search

### Vector Database
- ChromaDB with persistent storage
- Stores document chunks and metadata for similarity search

### Document Processing
- PDF extraction support
- DOCX extraction support
- TXT extraction support

---

## 4. Core Functionality

### 4.1 Document Upload
Users can upload supported files through the web interface or the API. The upload pipeline stores the file, extracts its text, cleans it, splits it into chunks, and indexes it for future retrieval.

### 4.2 Document Indexing
Each uploaded document is processed through a pipeline:

1. Save the uploaded file to disk
2. Extract raw text from the file
3. Clean and normalize the text
4. Chunk the text into smaller passage-sized sections
5. Generate embeddings for each chunk
6. Store the chunks in ChromaDB

### 4.3 Semantic Search and Retrieval
When a user asks a question, the application:

- Converts the question into an embedding
- Finds the most relevant document chunks
- Sends those chunks as context to the language model
- Generates an answer that references the retrieved content

### 4.4 Chat Interface
The frontend provides a conversational chat experience where users can ask questions and receive responses in a chat-style interface.

### 4.5 Document Management
The system allows users to view indexed documents and delete them from both the vector database and the local upload directory.

---

## 5. Key Features

### User-facing Features
- Modern and responsive document chat UI
- Drag-and-drop upload support
- Multiple file upload support
- Natural language document querying
- Source-backed answer generation
- Document listing and deletion
- Adjustable retrieval depth through the top-k setting
- Chat history with a clean message layout
- Upload progress indicators

### Technical Features
- Modular service-oriented backend architecture
- Separation of concerns between extraction, cleaning, chunking, retrieval, and LLM services
- Persistent vector storage using ChromaDB
- Structured metadata attached to each chunk
- API-based architecture suitable for future expansion
- Static frontend hosting through FastAPI

---

## 6. System Architecture

The application is organized around a layered architecture:

- API layer: routes for upload, chat, documents, and health
- Service layer: business logic for ingestion, retrieval, chunking, and LLM interaction
- Vector store layer: manages embeddings and similarity search
- Extractor layer: handles parsing of different document formats
- Frontend layer: provides the user interface for uploading and chatting

This separation makes the system easier to maintain and extend.

---

## 7. Main API Endpoints

### Health
- GET /api/v1/health -> checks whether the API is online

### Upload
- POST /api/v1/upload -> uploads and indexes a file

### Chat
- POST /api/v1/chat/query -> submits a question and receives an answer

### Documents
- GET /api/v1/documents -> lists indexed documents
- DELETE /api/v1/documents/{document_id} -> removes a document and its index entries

---

## 8. Project Structure

The repository is organized as follows:

- app/main.py: FastAPI application entry point
- app/api/: route definitions for health, upload, chat, and documents
- app/services/: business logic for upload, chat, retrieval, embeddings, chunking, and extraction
- app/extractors/: file-format-specific text extraction logic
- app/vectorstore/: vector database integration
- app/core/: shared application configuration and settings
- frontend/: static web interface files
- uploaded_files/: stored uploaded documents
- vector_db/: persistent ChromaDB storage

---

## 9. How the Application Works

A typical workflow looks like this:

1. A user uploads a document through the frontend.
2. The backend stores the file in the upload directory.
3. The document is extracted into plain text.
4. The text is cleaned and split into manageable chunks.
5. Each chunk is embedded and stored in ChromaDB.
6. When the user asks a question, the system retrieves the most relevant chunks.
7. Those chunks are used as context for the LLM.
8. The final answer is returned to the user.

This is the core RAG workflow used by the project.

---

## 10. Notable Implementation Highlights

Some important details that make the project practical include:

- Persistent document storage for uploaded files
- Persistent vector storage so indexed content survives restarts
- Source metadata attached to each chunk for traceability
- Built-in support for deleting documents and cleaning up related files
- A polished UI that makes the RAG experience feel interactive and modern

---

## 11. Current Limitations and Future Improvements

Although the project is functional, there are opportunities for improvement:

- Add user authentication and authorization
- Add support for more document types such as PowerPoint and spreadsheets
- Improve chunking quality with semantic or recursive chunking
- Add citation snippets in the answer itself rather than only in the UI
- Add observability, logging, and monitoring
- Add tests for the backend and frontend
- Add deployment support for Docker and cloud hosting
- Improve error handling and retry behavior for AI and embedding services

---

## 12. Summary

RAG Document Chat is a practical example of a modern AI-powered document assistant. It demonstrates how a web application can combine document ingestion, vector search, and language model generation into a usable chat experience. The architecture is clean, modular, and ready for further enhancement.
