"""
RAG (Retrieval-Augmented Generation) Engine
Main orchestrator: retrieves documents and generates answers with Grok LLM
"""

import logging
import time
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Complete RAG pipeline:
    1. Retrieve relevant documents
    2. Format context
    3. Send to Grok LLM
    4. Return answer with sources
    """

    def __init__(self, top_k: int = 5):
        """
        Initialize RAG engine

        Args:
            top_k: Number of documents to retrieve per query
        """
        self.top_k = top_k
        logger.info(f"RAGEngine initialized (top_k={top_k})")
    
    @staticmethod
    def _analyze_query_complexity(query: str) -> tuple:
        """
        Analyze query complexity to determine optimal retrieval strategy
        
        Args:
            query: User's question
            
        Returns:
            tuple: (complexity_level, top_k_suggestion, complexity_score)
            - complexity_level: 'simple', 'medium', or 'complex'
            - top_k_suggestion: Recommended number of documents
            - complexity_score: Numeric score (0-1)
        """
        from src.shared.config import settings
        
        # Word count analysis
        word_count = len(query.split())
        
        # Technical term detection
        technical_terms = {
            'budget', 'allocation', 'procurement', 'strategy', 'modernization',
            'deployment', 'personnel', 'expenditure', 'capabilities', 'systems',
            'technology', 'infrastructure', 'security', 'policy', 'framework',
            'analysis', 'comparison', 'implementation', 'performance', 'evaluation'
        }
        
        query_lower = query.lower()
        technical_term_count = sum(1 for term in technical_terms if term in query_lower)
        
        # Calculate complexity score (0-1)
        word_complexity = min(word_count / 30, 1.0)  # Max at 30 words
        technical_complexity = min(technical_term_count / 5, 1.0)  # Max at 5 terms
        complexity_score = (word_complexity * 0.6) + (technical_complexity * 0.4)
        
        # Determine complexity level and top_k
        if not settings.complexity_detection_enabled:
            # If disabled, use default
            return ('default', settings.rag_retrieval_top_k, complexity_score)
        
        if word_count < settings.complexity_simple_threshold and technical_term_count == 0:
            complexity_level = 'simple'
            top_k_suggestion = settings.complexity_simple_top_k
        elif word_count < settings.complexity_medium_threshold or technical_term_count <= 1:
            complexity_level = 'medium'
            top_k_suggestion = settings.complexity_medium_top_k
        else:
            complexity_level = 'complex'
            top_k_suggestion = settings.complexity_complex_top_k
        
        logger.debug(
            f"Query complexity analysis: level={complexity_level}, "
            f"words={word_count}, technical_terms={technical_term_count}, "
            f"score={complexity_score:.2f}, suggested_top_k={top_k_suggestion}"
        )
        
        return (complexity_level, top_k_suggestion, complexity_score)

    def generate_answer(
        self,
        query: str,
        db: Session,
        top_k: Optional[int] = None,
        document_type_filter: Optional[str] = None
    ) -> dict:
        """
        Generate an answer for a user query using RAG

        Args:
            query: User's question
            db: SQLAlchemy database session
            top_k: Number of documents to retrieve
            document_type_filter: Filter by document type

        Returns:
            dict with:
                - answer: Generated answer from Grok
                - sources: List of source documents with confidence
                - processing_time: Time taken to generate answer
                - model: Model used
                - confidence: Overall confidence score
                - error: Error message if failed
        """
        
        start_time = time.time()
        
        try:
            from src.services.retrieval import get_document_retriever
            from src.services.llm.gemini_client import get_gemini_client
            from src.services.llm.groq_client import get_groq_client
            from src.services.llm.grok_client import get_grok_client
            from src.shared.config import settings
            
            if top_k is None:
                # Auto-detect query complexity and adjust top_k
                complexity_level, auto_top_k, complexity_score = self._analyze_query_complexity(query)
                top_k = auto_top_k
                logger.info(f"RAG: Query complexity={complexity_level} (score={complexity_score:.2f}), auto top_k={top_k}")
            
            logger.info(f"RAG: Processing query: {query[:100]}...")
            
            # Step 1: Retrieve relevant documents
            logger.info("RAG: Retrieving documents...")
            retriever = get_document_retriever(top_k)
            retrieval_result = retriever.retrieve(
                query,
                top_k=top_k,
                db=db,
                document_type_filter=document_type_filter
            )
            
            if retrieval_result['status'] != 'success':
                return {
                    "answer": "",
                    "sources": [],
                    "processing_time": time.time() - start_time,
                    "model": "mixtral-8x7b-32768",
                    "confidence": 0.0,
                    "error": f"Retrieval failed: {retrieval_result.get('error', 'Unknown error')}"
                }
            
            # Extract context from retrieved chunks
            retrieved_chunks = retrieval_result['results']
            
            if not retrieved_chunks:
                logger.warning("No documents retrieved for query")
                return {
                    "answer": "I couldn't find any relevant documents to answer this question.",
                    "sources": [],
                    "processing_time": time.time() - start_time,
                    "model": "mixtral-8x7b-32768",
                    "confidence": 0.0,
                    "error": "No relevant documents found"
                }
            
            # Step 2: Format context for LLM
            logger.info("RAG: Formatting context...")
            context = self._format_context(retrieved_chunks)
            
            # Step 3: Generate answer - try LLM with fallback strategy
            logger.info("RAG: Attempting LLM generation (Groq → Grok → Fallback)...")
            groq_result = None
            grok_result = None
            llm_error = None
            
            # Try Gemini first (PRIMARY)
            try:
                if settings.gemini_api_key:
                    logger.info("RAG: Trying Gemini API (PRIMARY)...")
                    gemini = get_gemini_client(api_key=settings.gemini_api_key)
                    gemini_result = gemini.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.gemini_temperature,
                        max_tokens=1024
                    )
                    
                    if gemini_result.get('error'):
                        raise Exception(f"Gemini: {gemini_result['error']}")
                    
                    logger.info("✓ Gemini API succeeded")
                    return {
                        "answer": gemini_result['answer'],
                        "sources": self._extract_sources(retrieved_chunks),
                        "processing_time": time.time() - start_time,
                        "model": gemini_result.get('model', 'gemini-1.5-flash'),
                        "confidence": gemini_result.get('confidence', 0.90),
                        "error": None,
                        "tokens_used": gemini_result.get('tokens_used', 0)
                    }
                else:
                    logger.info("⚠ Gemini API key not configured, trying Groq...")
                    
            except Exception as gemini_error:
                llm_error = f"Gemini error: {str(gemini_error)}"
                logger.warning(f"⚠ {llm_error}, trying Groq...")
            
            # Try Groq as secondary
            try:
                if settings.groq_api_key:
                    logger.info("RAG: Trying Groq API (SECONDARY)...")
                    groq = get_groq_client(api_key=settings.groq_api_key)
                    groq_result = groq.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.grok_temperature,
                        max_tokens=1024
                    )
                    
                    if groq_result.get('error'):
                        raise Exception(f"Groq: {groq_result['error']}")
                    
                    logger.info("✓ Groq API succeeded")
                    return {
                        "answer": groq_result['answer'],
                        "sources": self._extract_sources(retrieved_chunks),
                        "processing_time": time.time() - start_time,
                        "model": groq_result.get('model', 'mixtral-8x7b-32768'),
                        "confidence": groq_result.get('confidence', 0.85),
                        "error": None,
                        "tokens_used": groq_result.get('tokens_used', 0)
                    }
                else:
                    logger.info("⚠ Groq API key not configured, trying Grok...")
                    
            except Exception as groq_error:
                llm_error = f"Groq error: {str(groq_error)}"
                logger.warning(f"⚠ {llm_error}, trying Grok...")
            
            # Try Grok as tertiary
            try:
                if settings.grok_api_key:
                    logger.info("RAG: Trying Grok API (TERTIARY)...")
                    grok = get_grok_client(api_key=settings.grok_api_key)
                    grok_result = grok.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.grok_temperature,
                        max_tokens=1024
                    )
                    
                    if grok_result.get('error'):
                        raise Exception(f"Grok: {grok_result['error']}")
                    
                    logger.info("✓ Grok API succeeded")
                    return {
                        "answer": grok_result['answer'],
                        "sources": self._extract_sources(retrieved_chunks),
                        "processing_time": time.time() - start_time,
                        "model": grok_result.get('model', 'grok-beta'),
                        "confidence": grok_result.get('confidence', 0.85),
                        "error": None,
                        "tokens_used": grok_result.get('tokens_used', 0)
                    }
                else:
                    logger.info("⚠ Grok API key not configured, using fallback...")
                    
            except Exception as grok_error:
                llm_error = f"{llm_error}; Grok error: {str(grok_error)}"
                logger.warning(f"⚠ Grok also failed: {str(grok_error)}, using fallback...")
            
            # Both LLMs failed - use fallback
            logger.warning(f"Using fallback (both LLMs failed): {llm_error}")
            answer = self._fallback_summarize(query, retrieved_chunks)
            sources = self._extract_sources(retrieved_chunks)
            processing_time = time.time() - start_time
            
            return {
                "answer": answer,
                "sources": sources,
                "processing_time": processing_time,
                "model": "fallback-retrieval",
                "confidence": 0.75,
                "error": llm_error
            }
            
        except Exception as e:
            error_msg = f"RAG pipeline error: {str(e)}"
            logger.error(error_msg)
            return {
                "answer": "",
                "sources": [],
                "processing_time": time.time() - start_time,
                "model": "mixtral-8x7b-32768",
                "confidence": 0.0,
                "error": error_msg
            }

    @staticmethod
    def _fallback_summarize(query: str, chunks: List[Dict]) -> str:
        """
        Generate a summary from retrieved documents when LLM is unavailable
        
        Args:
            query: User's question
            chunks: List of retrieved chunks
            
        Returns:
            Summary based on retrieved documents
        """
        
        if not chunks:
            return "No relevant documents found to answer your question."
        
        # Build summary from top chunks
        summary_parts = []
        summary_parts.append(f"Based on the retrieved documents:\n")
        
        for i, chunk in enumerate(chunks[:3], 1):  # Use top 3 results
            metadata = chunk.get('metadata', {})
            title = metadata.get('title', 'Document')
            score = chunk.get('similarity_score', 0)
            text = chunk.get('text', '')[:250]
            
            summary_parts.append(
                f"\n{i}. From '{title}' (confidence: {score:.1%}):\n"
                f"   {text}..."
            )
        
        summary_parts.append("\n\nNote: This is a summary from retrieved documents. " +
                           "For complete analysis, configure the Grok LLM API key.")
        
        return "".join(summary_parts)

    @staticmethod
    def _format_context(chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into context string for LLM

        Args:
            chunks: List of retrieved chunks

        Returns:
            Formatted context string
        """
        
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get('metadata', {})
            document_title = metadata.get('document_title', 'Unknown Document')
            
            context_parts.append(
                f"Document {i}: {document_title}\n"
                f"Content: {chunk['full_text']}\n"
                f"Relevance: {chunk['similarity_score']:.1%}\n"
            )
        
        return "\n---\n".join(context_parts)

    @staticmethod
    def _extract_sources(chunks: List[Dict]) -> List[Dict]:
        """
        Extract unique source documents from retrieved chunks

        Args:
            chunks: List of retrieved chunks

        Returns:
            List of source documents with metadata
        """
        
        sources = {}
        
        for chunk in chunks:
            metadata = chunk.get('metadata', {})
            doc_id = metadata.get('document_id')
            
            if not doc_id or doc_id in sources:
                continue
            
            sources[doc_id] = {
                "document_id": doc_id,
                "title": metadata.get('document_title', 'Unknown'),
                "url": metadata.get('source_url', ''),
                "document_type": metadata.get('document_type', 'unknown'),
                "similarity": chunk['similarity_score'],
                "snippet": chunk['text'][:200]
            }
        
        # Sort by similarity score
        sorted_sources = sorted(
            sources.values(),
            key=lambda x: x['similarity'],
            reverse=True
        )
        
        return sorted_sources


# Global instance
_rag_instance = None


def get_rag_engine(top_k: int = 5) -> RAGEngine:
    """Get or create RAG engine instance"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGEngine(top_k)
    return _rag_instance
