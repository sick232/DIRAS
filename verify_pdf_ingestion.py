#!/usr/bin/env python3
"""
Verification script to check ChromaDB and database contents
"""

import sys
import logging
from pathlib import Path
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).parent))

from src.shared.database import SessionLocal
from src.models.document import Document, DocumentChunk
from src.services.vectorstore import get_vector_store
from src.services.embeddings import get_embedding_generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_database():
    """Check database contents"""
    logger.info("="*70)
    logger.info("DATABASE VERIFICATION")
    logger.info("="*70)
    
    try:
        db = SessionLocal()
        
        # Count documents
        total_docs = db.query(Document).count()
        indexed_docs = db.query(Document).filter(Document.is_indexed == True).count()
        
        logger.info(f"📄 Total Documents: {total_docs}")
        logger.info(f"✓ Indexed Documents: {indexed_docs}")
        
        # Count chunks
        total_chunks = db.query(DocumentChunk).count()
        indexed_chunks = db.query(DocumentChunk).filter(DocumentChunk.is_indexed == True).count()
        
        logger.info(f"📑 Total Chunks: {total_chunks}")
        logger.info(f"✓ Indexed Chunks: {indexed_chunks}")
        
        # Get chunk counts per document
        logger.info("\n📋 Documents and their chunks:")
        documents = db.query(Document).order_by(Document.id.desc()).limit(12).all()
        
        for doc in documents:
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count()
            logger.info(f"  [{doc.id}] {doc.title[:50]} → {chunks} chunks (indexed: {doc.is_indexed})")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Database verification failed: {e}", exc_info=True)

def verify_chromadb():
    """Check ChromaDB contents"""
    logger.info("\n" + "="*70)
    logger.info("CHROMADB VERIFICATION")
    logger.info("="*70)
    
    try:
        vector_store = get_vector_store()
        collection_info = vector_store.get_collection_info()
        
        if collection_info:
            total_embeddings = collection_info.get('total_embeddings', 0)
            logger.info(f"✓ Total Embeddings in ChromaDB: {total_embeddings}")
            
            # Test retrieval
            if total_embeddings > 0:
                logger.info("\n🔍 Testing sample queries:")
                embedder = get_embedding_generator()
                
                test_queries = [
                    "defence procurement manual",
                    "financial delegation authority",
                    "standardization rules"
                ]
                
                for test_query in test_queries:
                    test_embedding = embedder.embed_text(test_query)
                    results = vector_store.collection.query(
                        query_embeddings=[test_embedding],
                        n_results=2
                    )
                    
                    if results and results.get('documents'):
                        logger.info(f"\n  Query: '{test_query}'")
                        for idx, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
                            score = 1 - results['distances'][0][idx-1] if results.get('distances') else 0
                            doc_title = metadata.get('document_title', 'Unknown')[:40]
                            logger.info(f"    [{idx}] {doc_title} (score: {score:.3f})")
                    else:
                        logger.warning(f"  Query '{test_query}': No results")
        else:
            logger.warning("Could not retrieve ChromaDB collection info")
            
    except Exception as e:
        logger.error(f"ChromaDB verification failed: {e}", exc_info=True)

def check_tracker():
    """Check ingestion tracker"""
    logger.info("\n" + "="*70)
    logger.info("INGESTION TRACKER")
    logger.info("="*70)
    
    try:
        import json
        tracker_file = Path("data/ingest_tracker.json")
        
        if tracker_file.exists():
            with open(tracker_file, 'r') as f:
                tracker = json.load(f)
            
            logger.info(f"✓ Tracked Files: {len(tracker)}")
            for file_path, info in sorted(tracker.items())[:5]:
                doc_id = info.get('document_id', 'unknown')
                ingested_at = info.get('ingested_at', 'unknown')
                logger.info(f"  {Path(file_path).name} → Doc ID: {doc_id}")
        else:
            logger.info("No tracker file found (will be created on first ingestion)")
            
    except Exception as e:
        logger.error(f"Tracker check failed: {e}", exc_info=True)

def main():
    """Run all verifications"""
    verify_database()
    verify_chromadb()
    check_tracker()
    
    logger.info("\n" + "="*70)
    logger.info("✅ VERIFICATION COMPLETE")
    logger.info("="*70)

if __name__ == "__main__":
    main()
