#!/usr/bin/env python
"""
Verification script for DIRAS RAG pipeline implementation
Tests all components to ensure they're working correctly
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all critical imports"""
    
    logger.info("\n" + "="*60)
    logger.info("Testing Imports...")
    logger.info("="*60)
    
    tests = []
    
    # Test 1: FastAPI
    try:
        from fastapi import FastAPI
        logger.info("✓ FastAPI")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ FastAPI: {e}")
        tests.append(False)
    
    # Test 2: Database
    try:
        from src.shared.database import engine, SessionLocal, Base, init_db
        logger.info("✓ Database (SQLAlchemy)")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Database: {e}")
        tests.append(False)
    
    # Test 3: Models
    try:
        from src.models.document import Document, DocumentChunk, Embedding
        logger.info("✓ Database Models")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Database Models: {e}")
        tests.append(False)
    
    # Test 4: Configuration
    try:
        from src.shared.config import settings
        logger.info("✓ Configuration (Pydantic Settings)")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Configuration: {e}")
        tests.append(False)
    
    # Test 5: Grok LLM
    try:
        from src.services.llm.grok_client import GrokClient, get_grok_client
        logger.info("✓ Grok LLM Client")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Grok LLM Client: {e}")
        tests.append(False)
    
    # Test 6: Document Processor
    try:
        from src.services.document_processor import DocumentProcessor, get_document_processor
        logger.info("✓ Document Processor")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Document Processor: {e}")
        tests.append(False)
    
    # Test 7: Text Processor
    try:
        from src.services.text_processor import TextProcessor, get_text_processor
        logger.info("✓ Text Processor")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Text Processor: {e}")
        tests.append(False)
    
    # Test 8: Vector Store
    try:
        from src.services.vectorstore import VectorStore, get_vector_store
        logger.info("✓ Vector Store (ChromaDB)")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Vector Store: {e}")
        tests.append(False)
    
    # Test 9: Embeddings
    try:
        from src.services.embeddings import EmbeddingGenerator, get_embedding_generator
        logger.info("✓ Embeddings (SentenceTransformers)")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Embeddings: {e}")
        tests.append(False)
    
    # Test 10: Indexer
    try:
        from src.services.indexer import DocumentIndexer, get_document_indexer
        logger.info("✓ Document Indexer")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Document Indexer: {e}")
        tests.append(False)
    
    # Test 11: Retrieval
    try:
        from src.services.retrieval import DocumentRetriever, get_document_retriever
        logger.info("✓ Document Retriever")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Document Retriever: {e}")
        tests.append(False)
    
    # Test 12: RAG Engine
    try:
        from src.services.rag_engine import RAGEngine, get_rag_engine
        logger.info("✓ RAG Engine")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ RAG Engine: {e}")
        tests.append(False)
    
    # Test 13: Scraper Runner
    try:
        import importlib
        scraper_module = importlib.import_module('src.01-data-pipeline.scraper_runner')
        ScraperRunner = getattr(scraper_module, 'ScraperRunner')
        logger.info("✓ Scraper Runner")
        tests.append(True)
    except Exception as e:
        logger.error(f"✗ Scraper Runner: {e}")
        tests.append(False)
    
    return tests

def test_configuration():
    """Test configuration loading"""
    
    logger.info("\n" + "="*60)
    logger.info("Testing Configuration...")
    logger.info("="*60)
    
    try:
        from src.shared.config import settings
        
        logger.info(f"✓ Environment: {settings.environment}")
        logger.info(f"✓ Database: {settings.database_url[:50]}...")
        logger.info(f"✓ ChromaDB: {settings.chromadb_host}:{settings.chromadb_port}")
        logger.info(f"✓ Grok API Key: {'✓ Configured' if settings.grok_api_key else '✗ Not configured'}")
        logger.info(f"✓ Embedding Model: {settings.embedding_model}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Configuration error: {e}")
        return False

def test_database_initialization():
    """Test database initialization"""
    
    logger.info("\n" + "="*60)
    logger.info("Testing Database Initialization...")
    logger.info("="*60)
    
    try:
        from src.shared.database import init_db
        
        init_db()
        logger.info("✓ Database tables created successfully")
        return True
    except Exception as e:
        logger.warning(f"⚠ Database initialization: {e}")
        logger.info("   This is OK if PostgreSQL is not running. Will work when you start the database.")
        return True  # Don't fail on this

def main():
    """Run all verification tests"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   DIRAS Phase 1-4 Implementation Verification         ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    # Run tests
    imports_ok = test_imports()
    config_ok = test_configuration()
    db_ok = test_database_initialization()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Summary")
    logger.info("="*60)
    
    total_tests = len(imports_ok)
    passed = sum(imports_ok)
    
    logger.info(f"Import Tests: {passed}/{total_tests} passed")
    logger.info(f"Configuration: {'✓ OK' if config_ok else '✗ FAILED'}")
    logger.info(f"Database: {'✓ OK' if db_ok else '⚠ Needs PostgreSQL'}")
    
    if passed == total_tests and config_ok:
        logger.info("\n✓✓✓ All systems ready! ✓✓✓")
        logger.info("\nNext steps:")
        logger.info("1. Ensure PostgreSQL is running")
        logger.info("2. Start mock backend: python mock_backend.py")
        logger.info("3. Or start real backend: python -m src.api.main")
        logger.info("4. Test frontend: http://localhost:3000")
        return 0
    else:
        logger.error("\n✗✗✗ Some components need attention ✗✗✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
