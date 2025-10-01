"""
Configuration Management
Following first principles: single source of truth for all settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Model Configuration
    default_model: str = "gpt-4"
    embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 4096
    temperature: float = 0.7
    
    # Vector Database
    chroma_persist_dir: str = "./data/chroma"
    collection_name: str = "zero_entropy_rag"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Memory & RAG Configuration
    max_context_length: int = 10
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
