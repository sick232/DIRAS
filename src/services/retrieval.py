"""
Retrieval Service
Retrieves relevant documents based on query
"""

import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DocumentRetriever:
    """
    Retrieves documents relevant to a query
    Uses vector similarity search on ChromaDB
    """

    def __init__(self, top_k: int = 5):
        """
        Initialize retriever

        Args:
            top_k: Default number of results to return
        """
        self.top_k = top_k
        logger.info(f"DocumentRetriever initialized (top_k={top_k})")

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        db: Session = None,
        document_type_filter: Optional[str] = None
    ) -> dict:
        """
        Retrieve relevant documents for a query

        Args:
            query: User's question/query
            top_k: Number of results to return (uses default if None)
            db: SQLAlchemy session for fetching metadata
            document_type_filter: Filter by document type (optional)

        Returns:
            dict with:
                - status: "success" or "failed"
                - query: original query
                - results: list of retrieved chunks with metadata
                - chunk_count: number of chunks retrieved
                - documents: list of unique documents
        """
        
        try:
            from src.services.embeddings import get_embedding_generator
            from src.services.vectorstore import get_vector_store
            
            if top_k is None:
                top_k = self.top_k
            
            logger.info(f"Retrieving top {top_k} results for query: {query[:100]}...")
            
            # Generate query embedding
            embedder = get_embedding_generator()
            query_embedding = embedder.embed_text(query)
            
            # Search vector store
            vector_store = get_vector_store()
            
            # Prepare filters if specified
            filters = None
            if document_type_filter and document_type_filter != "All Types":
                filters = {"document_type": document_type_filter}
            
            search_results = vector_store.search(
                query_embedding,
                top_k=top_k,
                filters=filters
            )
            
            if not search_results:
                logger.warning(f"No results found for query: {query}")
                return {
                    "status": "success",
                    "query": query,
                    "results": [],
                    "chunk_count": 0,
                    "documents": [],
                    "message": "No relevant documents found"
                }
            
            # Fetch full document metadata if database session provided
            results = []
            unique_docs = set()
            
            for result in search_results:
                chunk_data = {
                    "chunk_id": result['id'],
                    "text": result['document'][:500],  # Truncate for display
                    "full_text": result['document'],
                    "similarity_score": 1 - result['distance'],  # Convert distance to similarity
                    "metadata": result['metadata']
                }
                
                results.append(chunk_data)
                
                # Track unique documents
                if 'document_id' in result['metadata']:
                    unique_docs.add(result['metadata']['document_id'])
            
            logger.info(f"Retrieved {len(results)} chunks from {len(unique_docs)} documents")
            
            return {
                "status": "success",
                "query": query,
                "results": results,
                "chunk_count": len(results),
                "document_count": len(unique_docs),
                "documents": list(unique_docs)
            }
            
        except Exception as e:
            error_msg = f"Retrieval failed: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "failed",
                "query": query,
                "error": error_msg,
                "results": []
            }

    def retrieve_by_document(
        self,
        document_id: int,
        db: Session,
        top_k: int = None
    ) -> dict:
        """
        Retrieve all chunks for a specific document

        Args:
            document_id: ID of document
            db: SQLAlchemy session
            top_k: Max chunks to return

        Returns:
            dict with document chunks
        """
        
        try:
            from src.models.document import Document, DocumentChunk
            
            if top_k is None:
                top_k = self.top_k
            
            # Get document
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                return {"status": "failed", "error": f"Document {document_id} not found"}
            
            # Get chunks
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).limit(top_k).all()
            
            return {
                "status": "success",
                "document_id": document_id,
                "document_title": document.title,
                "chunks": [
                    {
                        "chunk_id": chunk.id,
                        "text": chunk.chunk_text,
                        "chunk_index": chunk.chunk_index
                    }
                    for chunk in chunks
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve document: {e}")
            return {"status": "failed", "error": str(e)}

    def set_top_k(self, top_k: int):
        """Update default top_k value"""
        self.top_k = top_k
        logger.info(f"Updated default top_k to {top_k}")


# Global instance
_retriever_instance = None


def get_document_retriever(top_k: int = 5) -> DocumentRetriever:
    """Get or create document retriever instance"""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = DocumentRetriever(top_k)
    return _retriever_instance
