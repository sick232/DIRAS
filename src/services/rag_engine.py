"""
RAG (Retrieval-Augmented Generation) Engine
Main orchestrator: retrieves documents and generates answers with Grok LLM
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
from src.services.excel_logger import save_query_log_to_excel, get_cached_query_result


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
        # Quick cache lookup in Excel logs
        try:
            cached = get_cached_query_result(query)
            if cached:
                processing_time = time.time() - start_time
                cached['processing_time'] = processing_time
                logger.info("RAG: Returning cached answer from Excel log")
                return cached
        except Exception as e:
            logger.warning(f"Cache lookup failed: {e}")
        debug_chunks = []
        retrieved_context = ""
        debug_prompt = ""
        gemini_output = ""
        groq_output = ""
        grok_output = ""
        fallback_output = ""
        llm_outputs = {
            "gemini": "",
            "groq": "",
            "grok": "",
            "fallback": ""
        }
        final_answer = ""
        model_used = ""
        confidence = 0.0
        sources = []

        try:
            from src.services.retrieval import get_document_retriever
            from src.services.llm.gemini_client import get_gemini_client
            from src.services.llm.groq_client import get_groq_client
            from src.services.llm.grok_client import get_grok_client
            from src.shared.config import settings
            
            if top_k is None:
                complexity_level, auto_top_k, complexity_score = self._analyze_query_complexity(query)
                top_k = auto_top_k
                logger.info(f"RAG: Query complexity={complexity_level} (score={complexity_score:.2f}), auto top_k={top_k}")
            
            logger.info(f"RAG: Processing query: {query[:100]}...")
            
            logger.info("RAG: Retrieving documents...")
            retriever = get_document_retriever(top_k)
            retrieval_result = retriever.retrieve(
                query,
                top_k=top_k,
                db=db,
                document_type_filter=document_type_filter
            )

            if retrieval_result['status'] != 'success':
                result = {
                    "answer": "",
                    "query": query,
                    "debug_chunks": [],
                    "retrieved_context": "",
                    "prompt_sent": "",
                    "gemini_raw_response": "",
                    "groq_raw_response": "",
                    "grok_raw_response": "",
                    "fallback_raw_response": "",
                    "final_answer": "",
                    "llm_outputs": llm_outputs,
                    "sources": [],
                    "processing_time": time.time() - start_time,
                    "model": "mixtral-8x7b-32768",
                    "model_used": "mixtral-8x7b-32768",
                    "confidence": 0.0,
                    "error": f"Retrieval failed: {retrieval_result.get('error', 'Unknown error')}"
                }
                self._append_debug_log({
                    "timestamp": datetime.utcnow().isoformat(),
                    "query": query,
                    "retrieved_chunks_text": "",
                    "retrieved_context": "",
                    "prompt_sent": "",
                    "gemini_output": "",
                    "groq_output": "",
                    "grok_output": "",
                    "fallback_output": "",
                    "final_answer": "",
                    "model": result["model"],
                    "processing_time": result["processing_time"],
                    "confidence": 0.0
                })
                return result
            
            retrieved_chunks = retrieval_result['results']
            debug_chunks = self._build_debug_chunks(retrieved_chunks)

            if not retrieved_chunks:
                logger.warning("No documents retrieved for query")
                result = {
                    "answer": "I couldn't find any relevant documents to answer this question.",
                    "query": query,
                    "debug_chunks": debug_chunks,
                    "retrieved_context": "",
                    "prompt_sent": "",
                    "gemini_raw_response": "",
                    "groq_raw_response": "",
                    "grok_raw_response": "",
                    "fallback_raw_response": "",
                    "final_answer": "",
                    "llm_outputs": llm_outputs,
                    "sources": [],
                    "processing_time": time.time() - start_time,
                    "model": "mixtral-8x7b-32768",
                    "model_used": "mixtral-8x7b-32768",
                    "confidence": 0.0,
                    "error": "No relevant documents found"
                }
                self._append_debug_log({
                    "timestamp": datetime.utcnow().isoformat(),
                    "query": query,
                    "retrieved_chunks_text": self._format_retrieved_chunks_for_excel(debug_chunks),
                    "retrieved_context": "",
                    "prompt_sent": "",
                    "gemini_output": "",
                    "groq_output": "",
                    "grok_output": "",
                    "fallback_output": "",
                    "final_answer": "",
                    "model": result["model"],
                    "processing_time": result["processing_time"],
                    "confidence": 0.0
                })
                return result

            logger.info("RAG: Formatting context...")
            context = self._format_context(retrieved_chunks)
            retrieved_context = context
            debug_prompt = (
                "You are a Defence Intelligence Assistant.\n\n"
                "DOCUMENTS:\n"
                f"{context}\n\n"
                "QUESTION:\n"
                f"{query}\n\n"
                "ANSWER:\n"
            )

            self._print_debug_terminal_sections(
                query=query,
                debug_chunks=debug_chunks,
                context=context,
                prompt_sent=debug_prompt,
                gemini_output=gemini_output,
                groq_output=groq_output,
                grok_output=grok_output,
                fallback_output=fallback_output,
                final_answer=final_answer
            )

            logger.info("RAG: Attempting LLM generation (Gemini → Groq → Grok → Fallback)...")
            llm_errors = []
            gemini_model = None
            groq_model = None
            grok_model = None
            gemini_conf = None
            groq_conf = None
            grok_conf = None

            # Gemini
            try:
                if settings.gemini_api_key:
                    logger.info("RAG: Calling Gemini (PRIMARY)")
                    gemini = get_gemini_client(api_key=settings.gemini_api_key)
                    gemini_result = gemini.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.gemini_temperature,
                        max_tokens=1024
                    )
                    if gemini_result.get('error'):
                        raise Exception(gemini_result.get('error'))
                    gemini_output = gemini_result.get('answer', '')
                    llm_outputs['gemini'] = gemini_output
                    gemini_model = gemini_result.get('model', 'gemini-2.5-flash')
                    gemini_conf = gemini_result.get('confidence', 0.90)
                else:
                    logger.info("⚠ Gemini API key not configured")
            except Exception as e:
                err = f"Gemini error: {e}"
                llm_errors.append(err)
                logger.warning(err)

            # Groq
            try:
                if settings.groq_api_key:
                    logger.info("RAG: Calling Groq (SECONDARY)")
                    groq = get_groq_client(api_key=settings.groq_api_key)
                    groq_result = groq.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.groq_temperature,
                        max_tokens=1024
                    )
                    if groq_result.get('error'):
                        raise Exception(groq_result.get('error'))
                    groq_output = groq_result.get('answer', '')
                    llm_outputs['groq'] = groq_output
                    groq_model = groq_result.get('model', 'mixtral-8x7b-32768')
                    groq_conf = groq_result.get('confidence', 0.85)
                else:
                    logger.info("⚠ Groq API key not configured")
            except Exception as e:
                err = f"Groq error: {e}"
                llm_errors.append(err)
                logger.warning(err)

            # Grok
            try:
                if settings.grok_api_key:
                    logger.info("RAG: Calling Grok (TERTIARY)")
                    grok = get_grok_client(api_key=settings.grok_api_key)
                    grok_result = grok.generate_answer(
                        query=query,
                        context=context,
                        temperature=settings.grok_temperature,
                        max_tokens=1024
                    )
                    if grok_result.get('error'):
                        raise Exception(grok_result.get('error'))
                    grok_output = grok_result.get('answer', '')
                    llm_outputs['grok'] = grok_output
                    grok_model = grok_result.get('model', 'grok-beta')
                    grok_conf = grok_result.get('confidence', 0.85)
                else:
                    logger.info("⚠ Grok API key not configured")
            except Exception as e:
                err = f"Grok error: {e}"
                llm_errors.append(err)
                logger.warning(err)

            # Always generate fallback summary
            fallback_output = self._fallback_summarize(query, retrieved_chunks)
            llm_outputs['fallback'] = fallback_output
            sources = self._extract_sources(retrieved_chunks)

            combined_analysis = (
                f"Gemini Analysis:\n{gemini_output or 'No Gemini output available.'}\n\n"
                f"Groq Analysis:\n{groq_output or 'No Groq output available.'}\n\n"
                f"Grok Analysis:\n{grok_output or 'No Grok output available.'}\n\n"
                f"Fallback Analysis:\n{fallback_output or 'No fallback output available.'}"
            )

            def _synthesize_report(question, combined_text, context_text, source_list):
                report_sections = []
                report_sections.append("EXECUTIVE SUMMARY:\n")
                report_sections.append(f"Question: {question}\n\n")
                report_sections.append("Overview:\n")
                report_sections.append(
                    "This report synthesizes intelligence from three independent model analyses and a fallback summary. "
                    "It highlights common findings, discrepancies, and operational implications.\n\n"
                )
                report_sections.append("Combined Analysis:\n")
                report_sections.append(combined_text + "\n\n")
                report_sections.append("Key Findings:\n")
                if gemini_output:
                    report_sections.append(f"- Gemini: {gemini_output.strip().splitlines()[0][:250]}...\n")
                if groq_output:
                    report_sections.append(f"- Groq: {groq_output.strip().splitlines()[0][:250]}...\n")
                if grok_output:
                    report_sections.append(f"- Grok: {grok_output.strip().splitlines()[0][:250]}...\n")
                if not any([gemini_output, groq_output, grok_output]):
                    report_sections.append("- No LLM model response available; using retrieved evidence and fallback summary.\n")
                report_sections.append("\nDetailed Analysis:\n")
                report_sections.append(combined_text + "\n\n")
                report_sections.append("Retrieved Context and Sources:\n")
                report_sections.append(context_text + "\n\n")
                if source_list:
                    report_sections.append("Cited Sources:\n")
                    for source in source_list:
                        title = source.get('title', source.get('document', 'Unknown'))
                        similarity = source.get('similarity', source.get('similarity_score', 0))
                        report_sections.append(f"- {title} (similarity: {similarity:.2f})\n")
                    report_sections.append("\n")
                report_sections.append("Implications and Recommendations:\n")
                report_sections.append("- Validate each model conclusion against official documentation.\n")
                report_sections.append("- Cross-check budgets, timelines, and operational claims before decision-making.\n")
                report_sections.append("- If discrepancies exist, prioritize the most consistently repeated intelligence themes.\n")
                return "".join(report_sections)

            final_answer = _synthesize_report(query, combined_analysis, context, sources)
            model_used = "multi-model-synthesis"
            confidence_values = [c for c in (gemini_conf, groq_conf, grok_conf) if isinstance(c, (int, float))]
            confidence = max(confidence_values) if confidence_values else 0.75
            processing_time = time.time() - start_time

            try:
                save_query_log_to_excel(
                    query=query,
                    retrieved_chunks=retrieved_chunks,
                    context=context,
                    prompt_sent=debug_prompt,
                    gemini_output=gemini_output,
                    groq_output=groq_output,
                    grok_output=grok_output,
                    fallback_output=fallback_output,
                    final_answer=final_answer,
                    model_used=model_used,
                    confidence=confidence,
                    processing_time=processing_time,
                )
            except Exception as e:
                logger.warning(f"Failed saving Excel log: {e}")

            self._print_debug_terminal_sections(
                query=query,
                debug_chunks=debug_chunks,
                context=context,
                prompt_sent=debug_prompt,
                gemini_output=gemini_output,
                groq_output=groq_output,
                grok_output=grok_output,
                fallback_output=fallback_output,
                final_answer=final_answer
            )

            return {
                "answer": final_answer,
                "query": query,
                "debug_chunks": debug_chunks,
                "retrieved_context": retrieved_context,
                "prompt_sent": debug_prompt,
                "gemini_raw_response": gemini_output,
                "groq_raw_response": groq_output,
                "grok_raw_response": grok_output,
                "fallback_raw_response": fallback_output,
                "final_answer": final_answer,
                "llm_outputs": llm_outputs,
                "sources": sources,
                "processing_time": processing_time,
                "model": model_used,
                "model_used": model_used,
                "confidence": confidence,
                "error": "; ".join(llm_errors) if llm_errors else None
            }
        except Exception as e:
            error_msg = f"RAG pipeline error: {str(e)}"
            logger.error(error_msg)
            return {
                "answer": "",
                "query": query,
                "debug_chunks": debug_chunks,
                "retrieved_context": retrieved_context,
                "prompt_sent": debug_prompt,
                "gemini_raw_response": gemini_output,
                "groq_raw_response": groq_output,
                "grok_raw_response": grok_output,
                "fallback_raw_response": fallback_output,
                "final_answer": final_answer,
                "llm_outputs": llm_outputs,
                "sources": sources,
                "processing_time": time.time() - start_time,
                "model": "mixtral-8x7b-32768",
                "model_used": "mixtral-8x7b-32768",
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
    def _build_debug_chunks(chunks: List[Dict]) -> List[Dict]:
        """
        Build debug chunk objects for logging and frontend display.
        """
        debug_chunks = []
        for chunk in chunks[:10]:
            metadata = chunk.get('metadata', {})
            debug_chunks.append({
                "document": metadata.get('document_title', 'Unknown Document'),
                "similarity": chunk.get('similarity_score', 0.0),
                "text": chunk.get('text', '')[:500]
            })
        return debug_chunks

    @staticmethod
    def _format_retrieved_chunks_for_excel(debug_chunks: List[Dict]) -> str:
        """
        Format retrieved chunks for Excel storage.
        """
        formatted_chunks = []
        for chunk in debug_chunks:
            formatted_chunks.append(
                f"Document: {chunk['document']}\n"
                f"Similarity: {chunk['similarity']:.4f}\n"
                f"Text:\n{chunk['text']}"
            )
        return "\n---\n".join(formatted_chunks)

    @staticmethod
    def _print_debug_terminal_sections(
        query: str,
        debug_chunks: List[Dict],
        context: str,
        prompt_sent: str,
        gemini_output: str,
        groq_output: str,
        grok_output: str,
        fallback_output: str,
        final_answer: str
    ) -> None:
        separator = "# " + "=" * 79
        print(separator)
        print("USER QUERY\n")
        print(query)

        print(separator)
        print("TOP RETRIEVED CHUNKS")
        for idx, chunk in enumerate(debug_chunks, 1):
            print(f"\n{idx}. Document Title: {chunk['document']}")
            print(f"Similarity Score: {chunk['similarity']:.4f}")
            print(f"Text: {chunk['text']}")

        print(separator)
        print("RETRIEVED CONTEXT")
        print(context)

        print(separator)
        print("PROMPT SENT TO LLM")
        print(prompt_sent)

        print(separator)
        print("GEMINI OUTPUT")
        print(gemini_output or "N/A")

        print(separator)
        print("GROQ OUTPUT")
        print(groq_output or "N/A")

        print(separator)
        print("GROK OUTPUT")
        print(grok_output or "N/A")

        print(separator)
        print("FALLBACK OUTPUT")
        print(fallback_output or "N/A")

        print(separator)
        print("FINAL ANSWER")
        print(final_answer)

    @staticmethod
    def _append_debug_log(record: Dict) -> None:
        """
        Append a row to the Excel debug log workbook.
        """
        try:
            # Delegate to centralized excel logger. The logger handles all exceptions.
            save_query_log_to_excel(
                query=record.get("query", ""),
                retrieved_chunks=record.get("retrieved_chunks", []),
                context=record.get("retrieved_context", ""),
                prompt_sent=record.get("prompt_sent", ""),
                gemini_output=record.get("gemini_output", ""),
                groq_output=record.get("groq_output", ""),
                grok_output=record.get("grok_output", ""),
                fallback_output=record.get("fallback_output", ""),
                final_answer=record.get("final_answer", ""),
                model_used=record.get("model", "") or record.get("model_used", ""),
                confidence=record.get("confidence", 0.0),
                processing_time=record.get("processing_time", 0.0),
            )
        except Exception as e:
            logger.warning(f"Failed delegating debug log to excel logger: {e}")

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
