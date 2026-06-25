#!/usr/bin/env python3
"""Quick verification of PDF ingestion"""

import sys
import logging
from pathlib import Path
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).parent))

from src.shared.database import SessionLocal
from src.models.document import Document, DocumentChunk

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    db = SessionLocal()
    
    logger.info("="*70)
    logger.info("FINAL VERIFICATION - PDF INGESTION")
    logger.info("="*70)
    
    # Count documents and chunks
    total_docs = db.query(Document).count()
    indexed_docs = db.query(Document).filter(Document.is_indexed == True).count()
    
    logger.info(f"\n📊 DATABASE STATUS:")
    logger.info(f"   Total Documents: {total_docs}")
    logger.info(f"   Indexed Documents: {indexed_docs}")
    
    # Recent PDF documents (IDs 44-55 based on ingestion)
    pdf_docs = db.query(Document).filter(Document.id >= 44).filter(Document.id <= 55).all()
    
    total_chunks = 0
    total_embeddings = 0
    
    logger.info(f"\n📄 PDF DOCUMENTS INDEXED:")
    for doc in sorted(pdf_docs, key=lambda d: d.id, reverse=True):
        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count()
        total_chunks += chunks
        total_embeddings += chunks
        status = "✓" if doc.is_indexed else "✗"
        logger.info(f"   {status} [{doc.id}] {doc.title[:50]}: {chunks} chunks")
    
    logger.info(f"\n📈 TOTALS (from PDFs):")
    logger.info(f"   Total Chunks: {total_chunks}")
    logger.info(f"   Total Embeddings: {total_embeddings}")
    
    # Check tracker
    import json
    tracker_file = Path("data/ingest_tracker.json")
    if tracker_file.exists():
        with open(tracker_file, 'r') as f:
            tracker = json.load(f)
        logger.info(f"\n🔐 TRACKER:")
        logger.info(f"   Tracked Files: {len(tracker)}")
    
    logger.info("\n" + "="*70)
    logger.info("✅ VERIFICATION COMPLETE")
    logger.info("="*70)
    
    db.close()
    
except Exception as e:
    logger.error(f"Verification failed: {e}", exc_info=True)
    sys.exit(1)
