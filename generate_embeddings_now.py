#!/usr/bin/env python
"""
Generate embeddings for all document chunks in SQLite
"""

import logging
from src.shared.database import SessionLocal
from src.models.document import Document, DocumentChunk, Embedding
from src.services.embeddings import get_embedding_generator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    session = SessionLocal()
    try:
        # Get embedding generator
        embedder = get_embedding_generator()
        logger.info("✓ Embedding generator initialized")
        
        # Get all chunks without embeddings
        chunks = session.query(DocumentChunk).filter(
            ~DocumentChunk.id.in_(
                session.query(Embedding.chunk_id)
            )
        ).all()
        
        logger.info(f"Found {len(chunks)} chunks without embeddings")
        
        # Generate embeddings
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding
                embedding_vec = embedder.embed_text(chunk.chunk_text)
                
                # Create and save embedding
                emb = Embedding(
                    chunk_id=chunk.id,
                    vector=embedding_vec,
                    model_name="all-MiniLM-L6-v2"
                )
                session.add(emb)
                
                if (i + 1) % 50 == 0:
                    session.commit()
                    logger.info(f"Progress: {i + 1}/{len(chunks)} embeddings created")
                
            except Exception as e:
                logger.error(f"Failed to embed chunk {chunk.id}: {e}")
                continue
        
        # Final commit
        session.commit()
        logger.info(f"✓ All {len(chunks)} embeddings created successfully")
        
        # Verify
        count = session.query(Embedding).count()
        logger.info(f"✓ Total embeddings in database: {count}")
        
    finally:
        session.close()

if __name__ == "__main__":
    main()
