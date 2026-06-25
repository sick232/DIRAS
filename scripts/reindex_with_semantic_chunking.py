#!/usr/bin/env python3
"""
Phase 3: Re-index Documents with Semantic-Aware Chunking
This script re-processes all documents with improved semantic-aware chunking
"""

import sys
import os
import time
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reindex_documents():
    """Re-index all documents with semantic-aware chunking"""
    
    print("\n" + "="*60)
    print("PHASE 3: RE-INDEX DOCUMENTS WITH SEMANTIC CHUNKING")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    try:
        from src.shared.database import SessionLocal
        from src.models.document import Document, DocumentChunk
        from src.services.text_processor import get_text_processor
        from src.services.indexer import DocumentIndexer
        from src.shared.config import settings
        
        db = SessionLocal()
        
        # Step 1: Clean existing chunks
        print("📋 Step 1: Clearing existing chunks...")
        existing_chunks = db.query(DocumentChunk).all()
        chunk_count_before = len(existing_chunks)
        
        for chunk in existing_chunks:
            db.delete(chunk)
        db.commit()
        
        print(f"   ✓ Removed {chunk_count_before} old chunks")
        
        # Step 2: Reset indexing status
        print("\n📋 Step 2: Resetting document indexing status...")
        documents = db.query(Document).all()
        total_docs = len(documents)
        
        for doc in documents:
            doc.is_indexed = False
        db.commit()
        
        print(f"   ✓ Reset {total_docs} documents to un-indexed state")
        
        # Step 3: Re-chunk documents with semantic awareness
        print(f"\n📋 Step 3: Re-chunking {total_docs} documents with semantic strategy...")
        
        processor = get_text_processor(
            chunk_size=settings.chunk_size_default,
            chunk_overlap=settings.chunk_overlap_default,
            strategy=settings.chunking_strategy
        )
        
        total_chunks_created = 0
        errors = []
        
        for idx, doc in enumerate(documents, 1):
            try:
                print(f"\n   [{idx}/{total_docs}] Processing: {doc.title[:50]}")
                
                if not doc.content_processed:
                    print(f"       ⚠ No content - skipping")
                    continue
                
                # Re-chunk with semantic awareness
                chunks = processor.chunk_document(
                    doc.content_processed,
                    document_id=doc.id,
                    db=db,
                    document_type=doc.document_type
                )
                
                total_chunks_created += len(chunks)
                
                print(f"       ✓ Created {len(chunks)} semantic chunks")
                print(f"         Type: {doc.document_type or 'unknown'}")
                print(f"         Avg size: {sum(len(c[0].split()) for c in chunks) // len(chunks) if chunks else 0} words")
                
            except Exception as e:
                error_msg = f"Error chunking document {doc.id}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                print(f"       ✗ Error: {str(e)}")
        
        print(f"\n   ✓ Total chunks created: {total_chunks_created}")
        
        if errors:
            print(f"\n   ⚠ Errors encountered: {len(errors)}")
            for error in errors[:5]:
                print(f"     - {error}")
        
        # Step 4: Re-index with embeddings
        print(f"\n📋 Step 4: Re-indexing with embeddings...")
        
        indexer = DocumentIndexer()
        result = indexer.index_all_documents(db, batch_size=32, skip_indexed=False)
        
        print(f"   ✓ Indexing result: {result['status']}")
        print(f"   ✓ Documents indexed: {result.get('total_documents', 0)}")
        print(f"   ✓ Chunks indexed: {result.get('total_chunks', 0)}")
        print(f"   ✓ Duration: {result.get('duration_seconds', 0):.1f}s")
        
        if result.get('errors'):
            print(f"   ⚠ Indexing errors: {len(result['errors'])}")
            for error in result['errors'][:3]:
                print(f"     - {error}")
        
        # Summary
        duration = time.time() - start_time
        
        print("\n" + "="*60)
        print("✅ PHASE 3 RE-INDEXING COMPLETE")
        print("="*60)
        print(f"Total time: {duration:.1f} seconds")
        print(f"\nResults:")
        print(f"  • Documents processed: {total_docs}")
        print(f"  • Chunks created: {total_chunks_created}")
        print(f"  • Strategy: {settings.chunking_strategy}")
        print(f"  • Chunk size: {settings.chunk_size_default} (default)")
        print(f"  • Preserve paragraphs: {settings.preserve_paragraph_boundaries}")
        print(f"\nConfiguration:")
        print(f"  • Simple doc chunks: {settings.chunk_size_simple}")
        print(f"  • Complex doc chunks: {settings.chunk_size_complex}")
        print(f"  • Min chunk size: {settings.min_chunk_size}")
        print("="*60 + "\n")
        
        return {
            "status": "success",
            "duration": duration,
            "documents_processed": total_docs,
            "chunks_created": total_chunks_created,
            "indexing_result": result
        }
        
    except Exception as e:
        logger.error(f"Re-indexing failed: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "duration": time.time() - start_time
        }

if __name__ == "__main__":
    result = reindex_documents()
    sys.exit(0 if result["status"] == "success" else 1)
