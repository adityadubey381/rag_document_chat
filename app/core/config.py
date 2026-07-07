import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "RAG Document Chat API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Storage Settings
    UPLOAD_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploaded_files"))
    VECTOR_DB_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../vector_db"))
    
    # AI Credentials
    OPENAI_API_KEY: str = "sk-dummy-key-for-development"  # Replace with real key in .env
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # Vector DB Preference
    VECTOR_STORE_TYPE: str = "chroma"  # 'chroma' or 'faiss'

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Ensure directories exist upon boot
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)