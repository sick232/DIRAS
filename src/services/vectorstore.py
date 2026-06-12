"""
Vector Store Service
Manages ChromaDB for storing and retrieving document embeddings
"""

import logging
from typing import List, Dict, Optional, Tuple
import json
import os
import shutil

logger = logging.getLogger(__name__)


class VectorStore:
    """
    ChromaDB vector store wrapper
    Handles embedding storage and semantic search
    """

    def __init__(self, persist_directory: str = "data/vectorstore", collection_name: str = "diras_documents"):
        """
        Initialize ChromaDB vector store

        Args:
            persist_directory: Directory for persistent storage
            collection_name: Name of ChromaDB collection
        """
        
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            
            # Disable anonymous telemetry in environments like Railway
            chroma_settings = ChromaSettings(anonymized_telemetry=False)
            
            # Initialize client using new PersistentClient API (v1.5.x+)
            self.client = chromadb.PersistentClient(path=persist_directory, settings=chroma_settings)
            self.collection_name = collection_name
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB vector store initialized. Collection: {collection_name}, Path: {persist_directory}")
            
        except ImportError:
            raise ImportError("ChromaDB not installed. Install with: pip install chromadb")
        except Exception as e:
            if "no such column: collections.topic" in str(e):
                logger.warning("ChromaDB schema mismatch detected; rebuilding vector store persistence")
                shutil.rmtree(persist_directory, ignore_errors=True)
                os.makedirs(persist_directory, exist_ok=True)

                chroma_settings = ChromaSettings(anonymized_telemetry=False)
                self.client = chromadb.PersistentClient(path=persist_directory, settings=chroma_settings)
                self.collection_name = collection_name
                self.collection = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info(f"ChromaDB vector store rebuilt and initialized. Collection: {collection_name}, Path: {persist_directory}")
            else:
                logger.error(f"Failed to initialize ChromaDB: {e}")
                raise

    def add_embeddings(
        self,
        chunk_ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict] = None
    ) -> bool:
        """
        Add embeddings to vector store

        Args:
            chunk_ids: List of unique chunk IDs
            embeddings: List of embedding vectors (384-dim)
            documents: List of chunk texts
            metadatas: Optional list of metadata dicts per chunk

        Returns:
            True if successful, False otherwise
        """
        
        try:
            if metadatas is None:
                metadatas = [{} for _ in chunk_ids]
            
            logger.info(f"Adding {len(chunk_ids)} embeddings to ChromaDB...")
            
            # Add to collection
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(chunk_ids)} embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add embeddings: {e}")
            return False

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Dict = None
    ) -> List[Dict]:
        """
        Search for similar chunks

        Args:
            query_embedding: Query embedding vector (384-dim)
            top_k: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of result dicts with:
                - id: chunk ID
                - document: chunk text
                - distance: similarity score (lower is better for cosine)
                - metadata: chunk metadata
        """
        
        try:
            logger.info(f"Searching ChromaDB for {top_k} similar chunks...")
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filters
            )
            
            # Transform results into standardized format
            if not results or not results['ids'] or not results['ids'][0]:
                logger.warning("No results found in ChromaDB")
                return []
            
            output = []
            for i, chunk_id in enumerate(results['ids'][0]):
                output.append({
                    'id': chunk_id,
                    'document': results['documents'][0][i] if results['documents'] else '',
                    'distance': results['distances'][0][i] if results['distances'] else 0.0,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                })
            
            logger.info(f"Found {len(output)} results")
            return output
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a chunk from the vector store

        Args:
            chunk_id: ID of chunk to delete

        Returns:
            True if successful
        """
        
        try:
            self.collection.delete(ids=[chunk_id])
            logger.info(f"Deleted chunk {chunk_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete chunk {chunk_id}: {e}")
            return False

    def get_collection_info(self) -> Dict:
        """
        Get information about the collection

        Returns:
            Dict with collection stats
        """
        
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_embeddings": count,
                "collection_object": self.collection
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}

    def persist(self):
        """Persist the collection to disk (auto-handled by PersistentClient)"""
        try:
            # PersistentClient automatically persists data, so this is a no-op
            # but we keep the method for API compatibility
            logger.info("ChromaDB data is automatically persisted")
        except Exception as e:
            logger.error(f"Error in persist: {e}")

    def clear_collection(self):
        """Clear all embeddings from collection (USE WITH CAUTION)"""
        try:
            # Get all IDs and delete
            results = self.collection.get()
            if results and results['ids']:
                self.collection.delete(ids=results['ids'])
            logger.warning(f"Cleared {len(results.get('ids', []))} embeddings from collection")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")


# Global instance
_store_instance: Optional[VectorStore] = None


def get_vector_store(
    persist_directory: str = "data/vectorstore",
    collection_name: str = "diras_documents"
) -> VectorStore:
    """Get or create vector store instance"""
    global _store_instance
    
    if _store_instance is None:
        _store_instance = VectorStore(persist_directory, collection_name)
    
    return _store_instance
