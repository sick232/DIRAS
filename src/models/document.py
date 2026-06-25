"""
Database models for DIRAS document management
SQLAlchemy ORM models for documents, chunks, and embeddings
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.shared.database import Base


class Document(Base):
    """
    Represents a downloaded and processed document
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source_url = Column(String(2000), unique=True, nullable=False, index=True)
    source_type = Column(String(100), nullable=True)  # e.g., "PIB", "MOD", "Parliamentary"
    document_type = Column(String(100), nullable=True)  # e.g., "Press Release", "Policy"
    
    # Content storage
    content_raw = Column(Text, nullable=True)  # Original downloaded text
    content_processed = Column(Text, nullable=True)  # OCR'd and cleaned text
    
    # Metadata
    published_date = Column(DateTime, nullable=True)
    downloaded_date = Column(DateTime, default=datetime.utcnow)
    
    # Status tracking
    status = Column(String(50), default="downloaded")  # downloaded, ocr_pending, ocr_complete, indexed
    ocr_confidence = Column(Float, nullable=True)  # OCR quality score (0-1)
    is_indexed = Column(Boolean, default=False)
    
    # Extra metadata as JSON (renamed to avoid SQLAlchemy conflict)
    doc_metadata = Column(JSON, nullable=True)  # Additional metadata dict
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Document(id={self.id}, title='{self.title}', status='{self.status}')>"


class DocumentChunk(Base):
    """
    Represents a chunk of text from a document
    Documents are split into chunks for embedding and retrieval
    """
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    
    # Content
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)  # Sequential index within document
    
    # Metadata
    token_count = Column(Integer, nullable=True)
    is_indexed = Column(Boolean, default=False)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    embedding = relationship("Embedding", back_populates="chunk", uselist=False, cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"


class Embedding(Base):
    """
    Stores embeddings for document chunks
    Each chunk gets a 384-dimensional vector embedding
    """
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("document_chunks.id"), nullable=False, unique=True, index=True)
    
    # Vector stored as JSON array for portability
    vector = Column(JSON, nullable=False)  # 384-dim array stored as JSON
    
    # Metadata
    model_name = Column(String(200), default="all-MiniLM-L6-v2")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chunk = relationship("DocumentChunk", back_populates="embedding")

    def __repr__(self):
        return f"<Embedding(id={self.id}, chunk_id={self.chunk_id}, model='{self.model_name}')>"


class IndexingLog(Base):
    """
    Tracks document indexing progress and metrics
    """
    __tablename__ = "indexing_logs"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    
    # Operation info
    operation = Column(String(100), nullable=False)  # "scrape", "ocr", "preprocess", "embed", "index"
    status = Column(String(50), nullable=False)  # "started", "completed", "failed"
    
    # Metrics
    duration_seconds = Column(Float, nullable=True)
    items_processed = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Extra metadata as JSON (renamed to avoid SQLAlchemy conflict)
    log_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<IndexingLog(id={self.id}, operation='{self.operation}', status='{self.status}')>"
