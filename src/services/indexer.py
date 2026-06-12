"""
Indexing Service
Orchestrates the process of creating and updating the vector index
"""

import logging
from typing import Optional
import time
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DocumentIndexer:
    """
    Indexes documents by generating embeddings and storing in ChromaDB
    Manages the complete indexing pipeline
    """

    def __init__(self):
        """Initialize document indexer"""
        logger.info("DocumentIndexer initialized")

    def index_all_documents(
        self,
        db: Session,
        batch_size: int = 32,
        skip_indexed: bool = True
    ) -> dict:
        """
        Index all documents that haven't been indexed yet

        Args:
            db: SQLAlchemy database session
            batch_size: Batch size for embedding generation
            skip_indexed: Skip already indexed documents

        Returns:
            dict with indexing results:
                - status: "success" or "failed"
                - total_documents: documents processed
                - total_chunks: chunks indexed
                - duration_seconds: time taken
                - errors: list of errors
        """
        
        start_time = time.time()
        errors = []
        
        try:
            from src.models.document import Document, DocumentChunk
            from src.services.embeddings import get_embedding_generator
            from src.services.vectorstore import get_vector_store
            
            logger.info("Starting document indexing process...")
            
            # Get vector store and embedder
            vector_store = get_vector_store()
            embedder = get_embedding_generator()
            
            # Report DB totals for diagnosis
            total_documents_in_db = db.query(Document).count()
            total_chunks_in_db = db.query(DocumentChunk).count()
            logger.info(f"📌 Indexer startup: {total_documents_in_db} total documents in DB, {total_chunks_in_db} total document chunks in DB")
            
            # Get unindexed documents
            query = db.query(Document).filter(Document.is_indexed == False)
            
            if skip_indexed:
                query = query.filter(Document.status == "ocr_complete")
            
            documents = query.all()
            total_docs = len(documents)
            
            logger.info(f"Found {total_docs} documents to index")
            
            if total_docs == 0:
                return {
                    "status": "success",
                    "total_documents": 0,
                    "total_chunks": 0,
                    "duration_seconds": 0,
                    "message": "No documents to index"
                }
            
            total_chunks_indexed = 0
            
            for doc_idx, document in enumerate(documents, 1):
                try:
                    logger.info(f"[{doc_idx}/{total_docs}] Indexing: {document.title[:50]}...")
                    
                    # Get all chunks for this document
                    chunks = db.query(DocumentChunk).filter(
                        DocumentChunk.document_id == document.id
                    ).all()
                    
                    logger.info(
                        f"📌 Document {document.id} ('{document.title[:60]}') has {len(chunks)} chunks"
                    )
                    
                    if not chunks:
                        logger.warning(
                            f"No chunks found for document {document.id} ('{document.title[:60]}')"
                        )
                        logger.info(
                            f"Document {document.id} status={document.status} content_processed_length={len(document.content_processed or '')}"
                        )
                        if document.status == "ocr_complete" and document.content_processed:
                            logger.info(f"Attempting chunk regeneration for document {document.id}")
                            from src.services.document_processor import get_document_processor
                            processor = get_document_processor()
                            regen_result = processor.process_document(document.id, db)
                            logger.info(f"Chunk regeneration result for document {document.id}: {regen_result}")
                            chunks = db.query(DocumentChunk).filter(
                                DocumentChunk.document_id == document.id
                            ).all()
                            logger.info(
                                f"After regeneration: document {document.id} has {len(chunks)} chunks"
                            )
                        
                    if not chunks:
                        logger.warning(
                            f"Skipping document {document.id} because no chunks are available"
                        )
                        continue
                    
                    # Prepare data for embedding
                    chunk_ids = [f"chunk_{chunk.id}" for chunk in chunks]
                    chunk_texts = [chunk.chunk_text for chunk in chunks]
                    
                    # Generate embeddings
                    embeddings = embedder.embed_batch(
                        chunk_texts,
                        batch_size=batch_size,
                        show_progress=False
                    )
                    
                    # Prepare metadata
                    metadatas = [
                        {
                            "document_id": str(document.id),
                            "document_title": document.title,
                            "chunk_index": chunk.chunk_index,
                            "source_url": document.source_url,
                            "document_type": document.document_type or "unknown"
                        }
                        for chunk in chunks
                    ]
                    
                    # Add to vector store
                    success = vector_store.add_embeddings(
                        chunk_ids,
                        embeddings,
                        chunk_texts,
                        metadatas
                    )
                    
                    if not success:
                        raise Exception("Failed to add embeddings to vector store")
                    
                    # Update database
                    document.is_indexed = True
                    for chunk in chunks:
                        chunk.is_indexed = True
                    
                    db.commit()
                    
                    total_chunks_indexed += len(chunks)
                    logger.info(f"Indexed {len(chunks)} chunks for document {document.id}")
                    
                except Exception as e:
                    error_msg = f"Failed to index document {document.id}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    db.rollback()
                    continue
            
            duration = time.time() - start_time
            
            logger.info(f"Indexing complete. Documents: {total_docs}, Chunks: {total_chunks_indexed}, Time: {duration:.1f}s")
            
            return {
                "status": "success" if len(errors) == 0 else "partial",
                "total_documents": total_docs,
                "total_chunks": total_chunks_indexed,
                "duration_seconds": duration,
                "errors": errors
            }
            
        except Exception as e:
            error_msg = f"Indexing failed: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "failed",
                "error": error_msg,
                "duration_seconds": time.time() - start_time
            }

    def index_document(
        self,
        document_id: int,
        db: Session
    ) -> dict:
        """
        Index a single document

        Args:
            document_id: ID of document to index
            db: SQLAlchemy session

        Returns:
            dict with result
        """
        
        try:
            from src.models.document import Document, DocumentChunk
            from src.services.embeddings import get_embedding_generator
            from src.services.vectorstore import get_vector_store
            
            # Get document
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                return {"status": "failed", "error": f"Document {document_id} not found"}
            
            # Get chunks
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).all()
            
            if not chunks:
                return {"status": "failed", "error": f"No chunks found for document {document_id}"}
            
            # Generate embeddings
            embedder = get_embedding_generator()
            chunk_texts = [chunk.chunk_text for chunk in chunks]
            embeddings = embedder.embed_batch(chunk_texts)
            
            # Add to vector store
            vector_store = get_vector_store()
            chunk_ids = [f"chunk_{chunk.id}" for chunk in chunks]
            metadatas = [
                {
                    "document_id": str(document.id),
                    "document_title": document.title,
                    "chunk_index": chunk.chunk_index
                }
                for chunk in chunks
            ]
            
            vector_store.add_embeddings(chunk_ids, embeddings, chunk_texts, metadatas)
            
            # Update database
            document.is_indexed = True
            for chunk in chunks:
                chunk.is_indexed = True
            db.commit()
            
            return {
                "status": "success",
                "document_id": document_id,
                "chunks_indexed": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            db.rollback()
            return {"status": "failed", "error": str(e)}

    def get_indexing_status(self, db: Session) -> dict:
        """
        Get current indexing status

        Args:
            db: SQLAlchemy session

        Returns:
            Status information
        """
        
        try:
            from src.models.document import Document, DocumentChunk
            
            total_docs = db.query(Document).count()
            indexed_docs = db.query(Document).filter(Document.is_indexed == True).count()
            
            total_chunks = db.query(DocumentChunk).count()
            indexed_chunks = db.query(DocumentChunk).filter(DocumentChunk.is_indexed == True).count()
            
            return {
                "total_documents": total_docs,
                "indexed_documents": indexed_docs,
                "pending_documents": total_docs - indexed_docs,
                "total_chunks": total_chunks,
                "indexed_chunks": indexed_chunks,
                "pending_chunks": total_chunks - indexed_chunks,
                "completion_percentage": round((indexed_chunks / total_chunks * 100) if total_chunks > 0 else 0, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to get indexing status: {e}")
            return {"error": str(e)}


# Global instance
_indexer_instance = None


def get_document_indexer() -> DocumentIndexer:
    """Get or create document indexer instance"""
    global _indexer_instance
    if _indexer_instance is None:
        _indexer_instance = DocumentIndexer()
    return _indexer_instance
