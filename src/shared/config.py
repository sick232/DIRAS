"""
Configuration management for DIRAS
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_log_level: str = "INFO"
    secret_key: str = "dev-secret-key-change-in-production"
    allowed_origins: str = "*"
    
    # Database
    database_url: str = "postgresql://diras:diras123@localhost:5432/diras"
    database_echo: bool = False
    
    # ChromaDB (Vector Database)
    chromadb_host: str = "localhost"
    chromadb_port: int = 8001
    chromadb_collection_name: str = "diras_documents"
    chromadb_persist_directory: str = "data/vectorstore"
    
    # Elasticsearch (Search)
    elasticsearch_host: str = "localhost"
    elasticsearch_port: int = 9200
    elasticsearch_index_name: str = "diras_documents"
    
    # LLM Configuration
    ollama_api_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024
    
    # Gemini LLM Configuration (PRIMARY)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.3
    
    # Grok LLM Configuration (SECONDARY)
    grok_api_key: str = ""
    grok_model: str = "grok-beta"
    grok_temperature: float = 0.3
    
    # Groq Configuration (TERTIARY)
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-70b-versatile"
    
    # LLM Retry Configuration (Phase 4B)
    llm_max_retries: int = 3
    llm_retry_delay: float = 1.0  # seconds
    llm_retry_backoff: float = 2.0  # exponential backoff multiplier
    llm_request_timeout: int = 30  # seconds
    llm_api_validation_enabled: bool = True
    
    # Models
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_batch_size: int = 32
    classifier_model_path: str = "models/classification/classifier.pkl"
    ner_model: str = "en_core_web_sm"
    
    # Paths
    data_raw_dir: str = "data/raw"
    data_processed_dir: str = "data/processed"
    data_embeddings_dir: str = "data/embeddings"
    models_dir: str = "models"
    logs_dir: str = "logs"
    
    # Scraping
    scraper_timeout: int = 30
    scraper_retry_attempts: int = 3
    scraper_delay_between_requests: float = 1.0
    
    # OCR
    ocr_languages: str = "en,hi"
    ocr_gpu: bool = True
    ocr_use_layout_parser: bool = True
    
    # RAG Configuration
    rag_retrieval_top_k: int = 15
    rag_context_window: int = 4000
    rag_reranker_top_k: int = 10
    hallucination_detection_enabled: bool = True
    
    # Query Complexity Detection (Phase 2)
    complexity_detection_enabled: bool = True
    complexity_simple_threshold: int = 10  # words
    complexity_medium_threshold: int = 20  # words
    complexity_simple_top_k: int = 5       # documents
    complexity_medium_top_k: int = 10      # documents
    complexity_complex_top_k: int = 15     # documents
    
    # Document Chunking (Phase 3 - Semantic-Aware)
    chunking_strategy: str = "semantic"
    chunk_size_default: int = 512
    chunk_overlap_default: int = 100
    chunk_size_simple: int = 300
    chunk_overlap_simple: int = 50
    chunk_size_complex: int = 768
    chunk_overlap_complex: int = 150
    preserve_paragraph_boundaries: bool = True
    min_chunk_size: int = 50
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/diras.log"
    log_max_bytes: int = 10485760
    log_backup_count: int = 5
    
    # Monitoring
    prometheus_port: int = 8002
    grafana_port: int = 3000
    metrics_enabled: bool = True
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = False
    
    def create_directories(self):
        """Create required directories if they don't exist"""
        dirs = [
            self.data_raw_dir,
            self.data_processed_dir,
            self.data_embeddings_dir,
            self.chromadb_persist_directory,
            self.models_dir,
            self.logs_dir,
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

# Create global settings instance
settings = Settings()

# Create required directories on import
settings.create_directories()
