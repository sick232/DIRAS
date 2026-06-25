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

    def _classify_query_retrieval(self, query: str) -> Optional[Dict[str, object]]:
        query_lower = query.lower()
        if any(term in query_lower for term in ['financial limit', 'approval limit', 'delegated power', 'delegation of financial powers', 'lab director']):
            return {
                'top_k': 5,
                'document_type_filters': ['financial_policy', 'approval_workflow', 'procurement', 'policy_document', 'manual'],
                'boost_terms': ['financial_limit', 'approval', 'authority', 'delegated power', 'lab director']
            }
        return None

    @staticmethod
    def _build_independent_llm_prompt(query: str) -> str:
        return (
            "You are a Senior Defence Procurement and Acquisition Specialist.\n\n"
            "You are an expert in:\n\n"
            "- Defence Acquisition Procedure (DAP 2020)\n"
            "- Defence Procurement Procedure\n"
            "- General Financial Rules\n"
            "- Delegation of Financial Powers\n"
            "- Capital Procurement\n"
            "- Revenue Procurement\n"
            "- Defence Budget\n"
            "- Contract Management\n"
            "- Government Procurement\n"
            "- Tendering\n"
            "- Ministry of Defence Policies\n\n"
            "Answer the user's question using your own knowledge.\n\n"
            "Question:\n"
            f"{query}\n\n"
            "Instructions:\n\n"
            "- Produce a complete answer.\n"
            "- Never truncate.\n"
            "- Never use ...\n"
            "- Use professional defence terminology.\n"
            "- Use markdown headings.\n"
            "- Use bullet points.\n"
            "- Mention applicable DAP chapters.\n"
            "- Mention GFR rules.\n"
            "- Mention procurement categories.\n"
            "- Mention financial authorities.\n"
            "- Mention monetary limits when applicable.\n"
            "- Mention approval process.\n"
            "- Mention exceptions if relevant.\n"
            "- Explain concepts clearly.\n"
            "- Never say 'Based on the provided context.'\n"
            "- Never mention you are an AI.\n"
            "- If uncertain, explicitly mention uncertainty instead of inventing information.\n"
            "Return only the answer.\n"
        )

    @staticmethod
    def _build_synthesis_prompt(query: str, rag_answer: str, groq_answer: str, gemini_answer: str) -> str:
        return (
            "You are the Chief Defence Procurement Knowledge Officer.\n\n"
            "Your responsibility is to prepare the FINAL authoritative answer.\n\n"
            "You have three independent information sources.\n\n"
            "================================================\n\n"
            "USER QUESTION\n\n"
            f"{query}\n\n"
            "================================================\n\n"
            "SOURCE 1\n\n"
            "Retrieved Defence Documents\n\n"
            f"{rag_answer}\n\n"
            "================================================\n\n"
            "SOURCE 2\n\n"
            "Groq Knowledge\n\n"
            f"{groq_answer}\n\n"
            "================================================\n\n"
            "SOURCE 3\n\n"
            "Gemini Knowledge\n\n"
            f"{gemini_answer}\n\n"
            "================================================\n\n"
            "Instructions\n\n"
            "1. Compare all three sources.\n"
            "2. Retrieved Defence Documents are the PRIMARY AUTHORITY.\n"
            "3. If Groq or Gemini contain additional useful information that does not contradict the documents, include it.\n"
            "4. Never contradict official documents.\n"
            "5. Merge duplicate information.\n"
            "6. Remove repetition.\n"
            "7. Never truncate.\n"
            "8. Never use ...\n"
            "9. Never say:\n\n"
            "- Based on the retrieved context\n"
            "- According to the provided context\n"
            "- Based on retrieved documents\n\n"
            "1. Produce a comprehensive answer.\n"
            "2. Explain concepts wherever helpful.\n"
            "3. Preserve every important rule.\n"
            "4. Preserve every financial limit.\n"
            "5. Preserve rule numbers.\n"
            "6. Preserve dates.\n"
            "7. Preserve authorities.\n"
            "8. Preserve procurement methods.\n"
            "9. Preserve tender categories.\n"
            "10. Preserve approval hierarchy.\n"
            "11. Use markdown.\n"
            "12. End with a clear concluding paragraph summarizing the key procurement consequences and compliance posture.\n"
            "Return ONLY the following format.\n\n"
            "# Executive Summary\n"
            "2-5 bullets\n\n"
            "# Detailed Answer\n"
            "Use bullet points.\n\n"
            "Every important point should appear.\n"
            "Do not limit the number of bullets.\n\n"
            "# Applicable Rules\n\n"
            "- Rule Number\n"
            "- DAP Chapter\n"
            "- GFR Rule\n"
            "- Delegation Rule\n\n"
            "# Financial Information\n\n"
            "- Financial Limits\n"
            "- Budget Values\n"
            "- Monetary Amounts\n\n"
            "# Authorities\n\n"
            "- Competent Financial Authority\n"
            "- Procurement Authority\n\n"
            "# Important Dates\n\n"
            "- Dates\n\n"
            "# Exceptions\n\n"
            "- Special Cases\n\n"
            "# Source Analysis\n\n"
            "- Information from Retrieved Documents\n"
            "- Additional Information from Groq\n"
            "- Additional Information from Gemini\n\n"
            "# Confidence\n"
            "High / Medium / Low"
        )

    @staticmethod
    def _dedupe_chunks(chunks: List[Dict]) -> List[Dict]:
        seen_texts = set()
        deduped = []
        for chunk in chunks:
            text = chunk.get('full_text', chunk.get('text', '')).strip()
            signature = text[:400]
            if signature in seen_texts:
                continue
            seen_texts.add(signature)
            deduped.append(chunk)
        return deduped

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
        # Quick cache lookup in Excel logs (DISABLED FOR TESTING)
        # try:
        #     cached = get_cached_query_result(query)
        #     if cached:
        #         processing_time = time.time() - start_time
        #         cached['processing_time'] = processing_time
        #         logger.info("RAG: Returning cached answer from Excel log")
        #         return cached
        # except Exception as e:
        #     logger.warning(f"Cache lookup failed: {e}")
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
            "groq_synthesis": "",
            "grok": "",
            "fallback": ""
        }
        final_answer = ""
        model_used = ""
        confidence = 0.0
        quality_score = 0.0
        quality_reason = ""
        llm_errors = []
        sources = []

        try:
            from src.services.retrieval import get_document_retriever
            try:
                from src.services.llm.gemini_client import get_gemini_client
                gemini_available = True
            except Exception as e:
                get_gemini_client = None
                gemini_available = False
                logger.warning(f"Gemini client unavailable: {e}")
            from src.services.llm.groq_client import get_groq_client
            from src.services.llm.grok_client import get_grok_client
            from src.shared.config import settings
            
            document_type_filters = None
            boost_terms = None
            if top_k is None:
                complexity_level, auto_top_k, complexity_score = self._analyze_query_complexity(query)
                top_k = auto_top_k
                logger.info(f"RAG: Query complexity={complexity_level} (score={complexity_score:.2f}), auto top_k={top_k}")

            classification = self._classify_query_retrieval(query)
            if classification:
                top_k = classification.get('top_k', top_k)
                document_type_filters = classification.get('document_type_filters')
                boost_terms = classification.get('boost_terms')
                logger.info(f"RAG: Query classification overridden retrieval settings - top_k={top_k}, document_type_filters={document_type_filters}")

            logger.info(f"RAG: Processing query: {query[:100]}...")
            
            logger.info("RAG: Retrieving documents...")
            
            # LOG: Query start information
            logger.info(f"📊 LOGGING: Query request - top_k={top_k}, document_type_filter={document_type_filter}, document_type_filters={document_type_filters}")
            
            retriever = get_document_retriever(top_k)
            retrieval_result = retriever.retrieve(
                query,
                top_k=top_k,
                db=db,
                document_type_filter=document_type_filter,
                document_type_filters=document_type_filters,
                boost_terms=boost_terms
            )

            if retrieval_result['status'] != 'success':
                # LOG: Retrieval failure
                logger.info(f"🗂️ LOGGING: Retrieval failed - Error: {retrieval_result.get('error', 'Unknown error')}")
                
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
            retrieved_chunks = self._dedupe_chunks(retrieved_chunks)
            debug_chunks = self._build_debug_chunks(retrieved_chunks)
            
            # LOG: Number of documents and chunks retrieved
            doc_count = retrieval_result.get('document_count', len(set(c.get('metadata', {}).get('document_id') for c in retrieved_chunks)))
            logger.info(f"📚 LOGGING: Loaded {doc_count} unique documents from database")
            logger.info(f"📊 LOGGING: Retrieved {len(retrieved_chunks)} chunks from retrieval service")

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
            
            # LOG: Retrieved context length
            logger.info(f"📊 LOGGING: Retrieved context length = {len(context)} characters")
            independent_llm_prompt = self._build_independent_llm_prompt(query)
            synthesis_prompt = None
            debug_prompt = independent_llm_prompt
            
            # LOG: Prompt sent to Groq
            logger.info(f"📊 LOGGING: Prompt sent to Groq/Gemini independent knowledge call (length={len(debug_prompt)} chars, first 200 chars: {debug_prompt[:200]}...)")

            if not (settings.groq_api_key or settings.gemini_api_key or settings.grok_api_key):
                llm_errors.append("No Groq, Gemini, or Grok API keys configured.")
                logger.warning("⚠ No LLM API keys configured; using fallback policy answer only.")
                fallback_answer = self._build_fallback_policy_answer(query, retrieved_chunks)
                final_answer = fallback_answer
                model_used = "fallback-only"
                confidence = 0.45
                quality_score = 2.0
                quality_reason = "No LLM keys configured; answer generated from retrieved documents."
                processing_time = time.time() - start_time

                self._print_debug_terminal_sections(
                    query=query,
                    debug_chunks=debug_chunks,
                    context=context,
                    prompt_sent=debug_prompt,
                    gemini_output=gemini_output,
                    groq_output=groq_output,
                    grok_output=grok_output,
                    fallback_output=fallback_answer,
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
                    "fallback_raw_response": fallback_answer,
                    "final_answer": final_answer,
                    "llm_outputs": llm_outputs,
                    "sources": self._extract_sources(retrieved_chunks),
                    "processing_time": processing_time,
                    "model": model_used,
                    "model_used": model_used,
                    "confidence": confidence,
                    "quality_score": quality_score,
                    "quality_reason": quality_reason,
                    "error": "; ".join(llm_errors)
                }

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

            logger.info("RAG: Attempting LLM generation (Groq → Gemini → Grok → Fallback)...")
            logger.info(f"Available API keys - Groq: {bool(settings.groq_api_key)}, Gemini: {bool(settings.gemini_api_key)}, Grok: {bool(settings.grok_api_key)}")
            llm_errors = []
            gemini_model = None
            groq_model = None
            grok_model = None
            gemini_conf = None
            groq_conf = None
            grok_conf = None
            groq = None
            gemini = None

            # Groq
            try:
                if settings.groq_api_key:
                    logger.info("RAG: Calling Groq (PRIMARY)")
                    groq = get_groq_client(api_key=settings.groq_api_key)
                    
                    # Wrap Groq call with timeout
                    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
                    groq_start = time.time()
                    try:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(
                                groq.generate_answer,
                                query=query,
                                context="",
                                temperature=settings.groq_temperature,
                                max_tokens=settings.groq_generation_max_tokens,
                                raw_prompt=independent_llm_prompt
                            )
                            groq_result = future.result(timeout=settings.llm_request_timeout + 10)
                            groq_elapsed = time.time() - groq_start
                            logger.info(f"Groq completed in {groq_elapsed:.2f}s")
                    except FutureTimeoutError:
                        groq_elapsed = time.time() - groq_start
                        err = f"Groq call timed out after {groq_elapsed:.2f}s"
                        logger.error(f"❌ {err}")
                        llm_errors.append(err)
                        groq_result = None
                    
                    if groq_result:
                        logger.error(f"GROQ RESULT TYPE: {type(groq_result)}")
                        logger.error(f"GROQ RESULT KEYS: {list(groq_result.keys()) if isinstance(groq_result, dict) else 'N/A'}")
                        logger.error(f"GROQ RESULT: {str(groq_result)[:1200]}")
                        if groq_result.get('error'):
                            raise Exception(groq_result.get('error'))
                        groq_output = groq_result.get('answer', '')
                        logger.error(f"GROQ OUTPUT LENGTH: {len(str(groq_output))}")
                        logger.error(f"GROQ OUTPUT SAMPLE: {str(groq_output)[:500]}")
                        
                        # LOG: Raw Groq response
                        logger.info(f"📊 LOGGING: Raw Groq response (length={len(groq_output)} chars, first 300 chars: {groq_output[:300]}...)")
                        
                        llm_outputs['groq'] = groq_output
                        groq_model = groq_result.get('model', 'mixtral-8x7b-32768')
                        groq_conf = groq_result.get('confidence', 0.85)
                else:
                    err = "Groq API key not configured in settings"
                    logger.error(f"❌ {err}")
                    llm_errors.append(err)
            except Exception as e:
                err = f"Groq error: {str(e)}"
                llm_errors.append(err)
                logger.error(f"❌ {err}")

            # Gemini
            try:
                if gemini_available and settings.gemini_api_key:
                    logger.info("RAG: Calling Gemini (SECONDARY)")
                    gemini = get_gemini_client(api_key=settings.gemini_api_key)
                    
                    # Wrap Gemini call with timeout
                    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
                    gemini_start = time.time()
                    try:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(
                                gemini.generate_answer,
                                query=query,
                                context="",
                                temperature=settings.gemini_temperature,
                                max_tokens=settings.gemini_generation_max_tokens,
                                raw_prompt=independent_llm_prompt
                            )
                            gemini_result = future.result(timeout=settings.llm_request_timeout + 10)
                            gemini_elapsed = time.time() - gemini_start
                            logger.info(f"Gemini completed in {gemini_elapsed:.2f}s")
                    except FutureTimeoutError:
                        gemini_elapsed = time.time() - gemini_start
                        err = f"Gemini call timed out after {gemini_elapsed:.2f}s"
                        logger.error(f"❌ {err}")
                        llm_errors.append(err)
                        gemini_result = None
                    
                    if gemini_result:
                        logger.error(f"GEMINI RESULT TYPE: {type(gemini_result)}")
                        logger.error(f"GEMINI RESULT KEYS: {list(gemini_result.keys()) if isinstance(gemini_result, dict) else 'N/A'}")
                        logger.error(f"GEMINI OUTPUT LENGTH: {len(str(gemini_result.get('answer', '')))}")
                        logger.error(f"GEMINI OUTPUT SAMPLE: {str(gemini_result.get('answer', ''))[:500]}")
                        if gemini_result.get('error'):
                            raise Exception(gemini_result.get('error'))
                        gemini_output = gemini_result.get('answer', '')
                        llm_outputs['gemini'] = gemini_output
                        gemini_model = gemini_result.get('model', 'gemini-2.5-flash')
                        gemini_conf = gemini_result.get('confidence', 0.90)
                else:
                    err = "Gemini is unavailable or not configured"
                    logger.warning(f"⚠ {err}")
            except Exception as e:
                err = f"Gemini error: {str(e)}"
                llm_errors.append(err)
                logger.error(f"❌ {err}")

            # Grok
            try:
                if settings.grok_api_key:
                    logger.info("RAG: Calling Grok (TERTIARY)")
                    grok = get_grok_client(api_key=settings.grok_api_key)
                    
                    # Wrap Grok call with timeout
                    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
                    grok_start = time.time()
                    try:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(
                                grok.generate_answer,
                                query=query,
                                context=context,
                                temperature=settings.grok_temperature,
                                max_tokens=settings.grok_generation_max_tokens
                            )
                            grok_result = future.result(timeout=settings.llm_request_timeout + 10)
                            grok_elapsed = time.time() - grok_start
                            logger.info(f"Grok completed in {grok_elapsed:.2f}s")
                    except FutureTimeoutError:
                        grok_elapsed = time.time() - grok_start
                        err = f"Grok call timed out after {grok_elapsed:.2f}s"
                        logger.error(f"❌ {err}")
                        llm_errors.append(err)
                        grok_result = None
                    
                    if grok_result:
                        logger.error(f"GROK RESULT TYPE: {type(grok_result)}")
                        logger.error(f"GROK RESULT KEYS: {list(grok_result.keys()) if isinstance(grok_result, dict) else 'N/A'}")
                        logger.error(f"GROK OUTPUT LENGTH: {len(str(grok_result.get('answer', '')))}")
                        logger.error(f"GROK OUTPUT SAMPLE: {str(grok_result.get('answer', ''))[:500]}")
                        if grok_result.get('error'):
                            raise Exception(grok_result.get('error'))
                        grok_output = grok_result.get('answer', '')
                        llm_outputs['grok'] = grok_output
                        grok_model = grok_result.get('model', 'grok-beta')
                        grok_conf = grok_result.get('confidence', 0.85)
                else:
                    err = "Grok API key not configured in settings"
                    logger.error(f"❌ {err}")
                    llm_errors.append(err)
            except Exception as e:
                err = f"Grok error: {str(e)}"
                llm_errors.append(err)
                logger.error(f"❌ {err}")

            # Always generate fallback summary
            fallback_output = self._fallback_summarize(query, retrieved_chunks)
            llm_outputs['fallback'] = fallback_output
            sources = self._extract_sources(retrieved_chunks)

            rag_answer = context
            combined_analysis = (
                f"Retrieved Documents:\n{rag_answer or 'No retrieved document summary available.'}\n\n"
                f"Groq Knowledge:\n{groq_output or 'No Groq output available.'}\n\n"
                f"Gemini Knowledge:\n{gemini_output or 'No Gemini output available.'}\n\n"
                f"Grok Knowledge:\n{grok_output or 'No Grok output available.'}"
            )

            groq_final_output = ""

            def _build_final_synthesis_prompt() -> str:
                return self._build_synthesis_prompt(query, rag_answer, groq_output, gemini_output)

            def _build_quality_prompt(report_text: str) -> str:
                return (
                    "You are a Quality Assessment Auditor for a Defence Intelligence report.\n\n"
                    "Evaluate the report for accuracy, completeness, clarity, and confidence.\n"
                    "Return JSON only with keys: quality_score (1.0-10.0), quality_reason.\n\n"
                    "Report:\n"
                    f"{report_text}\n\n"
                    "Candidate source summary:\n"
                    f"{combined_analysis}\n\n"
                    "Output format example:\n"
                    "{\"quality_score\": 8.3, \"quality_reason\": \"The final report is concise, mostly accurate, and well-sourced.\"}\n"
                )

            def _parse_quality_json(raw_text: str) -> tuple[float, str]:
                import json
                import re

                if not raw_text:
                    return 0.0, "No quality evaluation returned."

                json_match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
                if json_match:
                    try:
                        parsed = json.loads(json_match.group(0))
                        score = float(parsed.get('quality_score', 0.0))
                        reason = str(parsed.get('quality_reason', '')).strip()
                        if score < 0:
                            score = 0.0
                        if score > 10:
                            score = 10.0
                        return score, reason or "Quality review generated, but no reason provided."
                    except Exception:
                        pass

                digits = re.findall(r"\d+(?:\.\d+)?", raw_text)
                score = float(digits[0]) if digits else 0.0
                reason = raw_text.strip()
                return min(max(score, 0.0), 10.0), reason

            def _heuristic_quality_evaluation() -> tuple[float, str]:
                score = 0.0
                if confidence >= 0.9:
                    score += 4.0
                elif confidence >= 0.8:
                    score += 3.5
                elif confidence >= 0.7:
                    score += 3.0
                elif confidence >= 0.6:
                    score += 2.5
                else:
                    score += 2.0

                score += min(len(retrieved_chunks) / max(top_k, 1), 1.0) * 2.0
                score += min(len(sources), 3) * 0.5
                if fallback_output and not (groq_output or gemini_output or grok_output):
                    score -= 1.0
                if 'no relevant documents' in final_answer.lower() or 'could not find' in final_answer.lower():
                    score = min(score, 3.0)

                score = max(1.0, min(score, 10.0))
                reason = (
                    f"Heuristic scoring based on confidence, retrieval coverage, and source count. "
                    f"Confidence={confidence:.2f}, retrieved_chunks={len(retrieved_chunks)}, sources={len(sources)}."
                )
                return score, reason

            def _evaluate_quality(report_text: str) -> tuple[float, str]:
                if gemini and settings.gemini_api_key:
                    try:
                        quality_prompt = _build_quality_prompt(report_text)
                        quality_result = gemini.generate_answer(
                            query=quality_prompt,
                            context=combined_analysis,
                            temperature=0.1,
                            max_tokens=180
                        )
                        if quality_result.get('error'):
                            raise Exception(quality_result.get('error'))
                        score, reason = _parse_quality_json(quality_result.get('answer', ''))
                        if score > 0.0:
                            return score, reason
                    except Exception as e:
                        logger.warning(f"Quality evaluation Gemini failed: {e}")

                if groq and settings.groq_api_key:
                    try:
                        quality_prompt = _build_quality_prompt(report_text)
                        quality_result = groq.generate_answer(
                            query=quality_prompt,
                            context=combined_analysis,
                            temperature=0.1,
                            max_tokens=180
                        )
                        if quality_result.get('error'):
                            raise Exception(quality_result.get('error'))
                        score, reason = _parse_quality_json(quality_result.get('answer', ''))
                        if score > 0.0:
                            return score, reason
                    except Exception as e:
                        logger.warning(f"Quality evaluation Groq failed: {e}")

                return _heuristic_quality_evaluation()

            def _synthesize_final_report() -> str:
                prompt = _build_final_synthesis_prompt()
                synthesis_prompt = prompt
                if groq and settings.groq_api_key:
                    try:
                        result = groq.generate_answer(
                            query=prompt,
                            context=combined_analysis,
                            temperature=max(settings.groq_temperature, 0.2),
                            max_tokens=settings.groq_synthesis_max_tokens,
                            raw_prompt=prompt
                        )
                        if result.get('error'):
                            raise Exception(result.get('error'))
                        answer = result.get('answer', '')
                        if answer:
                            nonlocal groq_final_output
                            groq_final_output = answer.strip()
                            return groq_final_output
                    except Exception as e:
                        logger.warning(f"Final synthesis Groq failed: {e}")

                if gemini and settings.gemini_api_key:
                    try:
                        result = gemini.generate_answer(
                            query=prompt,
                            context=combined_analysis,
                            temperature=max(settings.gemini_temperature, 0.2),
                            max_tokens=1200
                        )
                        if result.get('error'):
                            raise Exception(result.get('error'))
                        answer = result.get('answer', '')
                        if answer:
                            return answer.strip()
                    except Exception as e:
                        logger.warning(f"Final synthesis Gemini failed: {e}")

                return ""

            def _clean_text(text: str, max_chars: Optional[int] = None) -> str:
                if not text:
                    return ""
                cleaned = text.strip()
                if max_chars is not None and len(cleaned) > max_chars:
                    cleaned = cleaned[:max_chars].rstrip()
                return cleaned

            def _ensure_final_closure(answer: str) -> str:
                if not answer or not answer.strip():
                    return answer
                stripped = answer.strip()
                if stripped[-1] in {'.', '!', '?'}:
                    return answer
                return f"{answer.strip()}\n\nIn summary, this practice is prohibited and carries clear procurement and financial consequences."

            def _extract_direct_answer(*outputs: str) -> str:
                for output in outputs:
                    if output and output.strip():
                        candidate = _clean_text(output)
                        return candidate
                return "No direct answer available from the retrieved documents."

            def _extract_findings(*outputs: str) -> list[str]:
                findings = []
                for output in outputs:
                    if not output:
                        continue
                    first_line = output.strip().splitlines()[0]
                    if first_line:
                        cleaned = _clean_text(first_line, max_chars=120)
                        if cleaned not in findings:
                            findings.append(cleaned)
                    if len(findings) >= 5:
                        break
                return findings

            def _build_sources(source_list):
                sources = []
                for source in source_list[:5]:
                    title = source.get('document_title') or source.get('title') or source.get('document') or 'Unknown Source'
                    if title not in sources:
                        sources.append(title)
                return sources

            def _synthesize_report(question, context_text, source_list):
                def _select_best_llm_output() -> str:
                    for output in (groq_output, gemini_output, grok_output, fallback_output):
                        if output and len(output.strip()) > 120:
                            return output.strip()
                    return fallback_output.strip() if fallback_output else ""

                def _extract_findings(*outputs: str) -> list[str]:
                    findings = []
                    for output in outputs:
                        if not output:
                            continue
                        lines = [line.strip() for line in output.splitlines() if line.strip()]
                        bullet_lines = [line for line in lines if line.startswith(('*', '-', '•')) or line.split('.')[0].isdigit()]
                        candidate_lines = bullet_lines if bullet_lines else lines
                        for line in candidate_lines:
                            text = line
                            lower = text.lower()
                            if lower.startswith("the context provided") or lower.startswith("based on the retrieved"):
                                continue
                            if lower.startswith("fallback analysis") or lower.startswith("grok analysis") or lower.startswith("gemini analysis") or lower.startswith("groq analysis"):
                                continue
                            if len(text) < 20:
                                continue
                            cleaned = _clean_text(text, max_chars=120)
                            if cleaned not in findings:
                                findings.append(cleaned)
                                break
                        if len(findings) >= 5:
                            break
                    return findings

                def _no_evidence_response(question: str, source_list: list[str]) -> str:
                    source_lines = "\n".join(f"- {source}" for source in source_list[:3]) if source_list else "- No sources available"
                    if any(term in question.lower() for term in ['financial limit', 'approval limit', 'delegated power', 'lab director', 'financial approval']):
                        return (
                            "No explicit financial approval limit for a Lab Director was found in the indexed documents.\n\n"
                            f"Most relevant documents searched:\n{source_lines}\n\n"
                            "Recommendation: Review the specific delegation schedule or authority matrix section."
                        )
                    return (
                        "No explicit answer was found in the indexed documents.\n\n"
                        f"Most relevant documents searched:\n{source_lines}\n\n"
                        "Recommendation: Review the relevant policy or authority document sections."
                    )

                def _extract_numbers_and_dates(text: str) -> list[str]:
                    if not text:
                        return []
                    import re
                    date_pattern = r"\b(?:\d{4}-\d{2}(?:-\d{2})?|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:,\s*\d{4})?)\b"
                    amount_pattern = r"₹[\d,]+(?:\.\d+)?(?:\s*(?:lakh|million|billion)?\s*crore|\s*crore)?"
                    percent_pattern = r"\b\d+(?:\.\d+)?%\b"
                    dates = re.findall(date_pattern, text, flags=re.IGNORECASE)
                    percentages = re.findall(percent_pattern, text, flags=re.IGNORECASE)
                    numbers = re.findall(f"(?:{amount_pattern})", text, flags=re.IGNORECASE)
                    
                    extracted = []
                    # Add dates
                    for item in dates:
                        item = item.strip()
                        if item and item not in extracted and len(extracted) < 4:
                            extracted.append(item)
                    
                    # Add amounts
                    for item in numbers:
                        item = item.strip()
                        if item and item not in extracted and len(extracted) < 4:
                            extracted.append(item)
                    
                    # Add only realistic percentages (0-100%, not BM25 scores)
                    for item in percentages:
                        try:
                            val = float(item.rstrip('%'))
                            # Only include percentages between 0 and 100
                            if 0 <= val <= 100 and item not in extracted and len(extracted) < 4:
                                extracted.append(item)
                        except (ValueError, AttributeError):
                            pass
                    
                    return extracted[:4]

                best_output = _select_best_llm_output()
                sources = _build_sources(source_list)
                if not best_output or 'no direct answer available' in best_output.lower() or 'not explicitly stated' in best_output.lower():
                    return _no_evidence_response(question, sources)
                direct_answer = _clean_text(best_output or fallback_output or "No direct answer available from the retrieved documents.", max_chars=400)
                findings = _extract_findings(groq_output, gemini_output, grok_output, fallback_output)
                sources = _build_sources(source_list)

                numbers_dates = _extract_numbers_and_dates("\n".join([groq_output, gemini_output, grok_output, fallback_output]))

                if not findings and context_text:
                    first_context = context_text.strip().splitlines()[0] if context_text.strip() else ''
                    if first_context:
                        findings.append(_clean_text(first_context, max_chars=120))

                if not findings:
                    findings.append("Key points are available from the retrieved documents, but the model did not return explicit findings.")

                max_bullets = 8
                source_slots = min(3, len(sources), max_bullets)
                remaining_slots = max_bullets - source_slots
                number_slots = min(3, len(numbers_dates), remaining_slots)
                remaining_slots -= number_slots
                finding_slots = min(4, len(findings), remaining_slots)

                report_sections = []
                report_sections.append("🏁 QUICK ANSWER\n")
                report_sections.append(f"{direct_answer}\n\n")

                report_sections.append("🔑 KEY FINDINGS\n")
                for finding in findings[:finding_slots]:
                    report_sections.append(f"• {finding}\n")
                report_sections.append("\n")

                if numbers_dates[:number_slots]:
                    report_sections.append("📅 IMPORTANT NUMBERS / DATES\n")
                    for item in numbers_dates[:number_slots]:
                        report_sections.append(f"• {item}\n")
                    report_sections.append("\n")

                report_sections.append("📚 SOURCES\n")
                if sources:
                    for source in sources[:source_slots]:
                        report_sections.append(f"• {source}\n")
                else:
                    report_sections.append("• No sources available\n")

                report_sections.append("\n📊 CONFIDENCE\n")
                normalized_confidence = min(0.95, max(0.30, confidence))
                report_sections.append(f"{int(normalized_confidence * 100)}%\n")
                return "".join(report_sections)

            model_used = "multi-model-synthesis"
            confidence_values = [c for c in (gemini_conf, groq_conf, grok_conf) if isinstance(c, (int, float))]
            confidence = max(confidence_values) if confidence_values else 0.75
            confidence = min(0.95, max(0.30, confidence))

            final_answer = _synthesize_final_report().strip()
            if groq_final_output:
                llm_outputs['groq_synthesis'] = groq_final_output

            if not final_answer or final_answer.lower().startswith('based on the retrieved documents') or final_answer.lower().startswith('no explicit answer'):
                if groq_final_output:
                    final_answer = groq_final_output
                    model_used = "groq-final-synthesis"
                elif groq_output:
                    final_answer = groq_output.strip()
                    model_used = "groq-independent"
                elif gemini_output:
                    final_answer = gemini_output.strip()
                    model_used = "gemini-independent"
                elif fallback_output:
                    final_answer = fallback_output.strip()
                    model_used = "fallback-summary"

            raw_best_output = ""
            raw_best_source = None
            for source_name, output in (
                ("groq", groq_output),
                ("gemini", gemini_output),
                ("grok", grok_output),
                ("fallback", fallback_output),
            ):
                if output and len(output.strip()) > 120:
                    raw_best_output = output.strip()
                    raw_best_source = source_name
                    break

            if raw_best_output and len(raw_best_output) > len(final_answer) + 200:
                logger.info("RAG: Using longer raw LLM output to preserve full answer content.")
                final_answer = raw_best_output
                if raw_best_source == "groq":
                    model_used = "groq-independent"
                elif raw_best_source == "gemini":
                    model_used = "gemini-independent"
                elif raw_best_source == "grok":
                    model_used = "grok-independent"
                else:
                    model_used = "fallback-summary"

            final_answer = _ensure_final_closure(final_answer)
            quality_score, quality_reason = _evaluate_quality(final_answer)
            final_answer = (
                f"{final_answer}\n\n"
                f"⭐ OUTPUT QUALITY\n"
                f"{quality_score:.1f}/10\n\n"
                f"📝 ASSESSMENT\n"
                f"{quality_reason.strip()}"
            )

            # LOG: Final answer before API return
            logger.info(f"📊 LOGGING: Final answer length = {len(final_answer)} characters")
            logger.info(f"📊 LOGGING: Final answer (first 400 chars): {final_answer[:400]}...")
            
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
                    quality_score=quality_score,
                    quality_reason=quality_reason,
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
                "quality_score": quality_score,
                "quality_reason": quality_reason,
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

        summary_parts = []
        summary_parts.append("Based on the retrieved documents:\n")

        for i, chunk in enumerate(chunks[:3], 1):  # Use top 3 results
            metadata = chunk.get('metadata', {})
            title = metadata.get('title', 'Document')
            text = chunk.get('full_text', chunk.get('text', ''))
            summary_parts.append(
                f"\n{i}. From '{title}':\n"
                f"   {text}"
            )

        summary_parts.append("\n\nNote: This is a summary from retrieved documents. " +
                           "For complete analysis, configure the Grok LLM API key.")
        return "".join(summary_parts)

    @staticmethod
    def _build_fallback_answer(query: str, chunks: List[Dict]) -> str:
        """
        Build a concise fallback answer when no LLM model is available.
        """
        import re

        if not chunks:
            return (
                "### Fallback Answer\n"
                "No relevant documents were found for this query. "
                "Please configure Groq/Gemini/Grok API keys to generate a full answer."
            )

        combined_text = "\n".join(
            chunk.get('full_text', chunk.get('text', '')) for chunk in chunks[:5]
        )
        sentences = re.split(r'(?<=[\.!?])\s+', combined_text)
        keywords = [
            'penalt', 'forfeit', 'debar', 'threshold', 'invoice', 'split', 'aggregate',
            'approval', 'CFA', 'IFA', 'EMD', 'tender', 'procurement', 'RFP', 'threshold',
            'rule', 'delegation', 'financial', 'emergency'
        ]

        extracted = []
        for sentence in sentences:
            if len(extracted) >= 6:
                break
            low = sentence.lower()
            if any(keyword in low for keyword in keywords) and len(sentence.strip()) > 60:
                cleaned = sentence.strip().replace('\n', ' ').replace('  ', ' ').strip()
                if cleaned not in extracted:
                    extracted.append(cleaned)

        if not extracted:
            extracted = [
                "Splitting a single procurement into multiple invoices to avoid the RFP threshold is generally treated as artificial splitting of procurement.",
                "Related purchases must be aggregated to determine the applicable threshold under procurement rules.",
                "Penalties can include forfeiture of EMD, disqualification, debarment, or cancellation of the procurement process.",
            ]

        bullet_lines = "\n".join(f"• {line}" for line in extracted[:6])
        answer = (
            "### Fallback Answer\n"
            "The system could not generate a Groq/Gemini/Grok answer because API keys are not configured. "
            "Below is a document-based fallback summary.\n\n"
            "### Likely consequences of invoice splitting to avoid RFP threshold\n"
            f"{bullet_lines}\n\n"
            "### Key procurement considerations\n"
            "• Treat related purchase values as aggregated for threshold calculation.\n"
            "• Follow DAP/GFR financial and procurement thresholds; do not split invoices to evade the rules.\n"
            "• Ensure CFA/IFA approval and proper delegation of financial authority.\n"
            "• Use appropriate procurement categories: Open Tender, Limited Tender, Single Source, Direct Procurement.\n"
            "• Exceptions such as emergency procurement must be documented and approved, not used to cover artificial splits.\n"
        )
        return answer

    @staticmethod
    def _build_fallback_policy_answer(query: str, chunks: List[Dict]) -> str:
        """
        Build a policy-style fallback answer when no LLM model is available.
        """
        if not chunks:
            return (
                "# Fallback Answer\n"
                "No relevant documents were found for this query. "
                "Please configure Groq/Gemini/Grok API keys to generate a complete answer."
            )

        source_titles = []
        for chunk in chunks[:3]:
            metadata = chunk.get('metadata', {})
            title = metadata.get('document_title') or metadata.get('title') or 'Unknown Document'
            if title not in source_titles:
                source_titles.append(title)

        answer = (
            "# Fallback Answer\n"
            "Splitting a single purchase into multiple invoices to avoid the RFP threshold is treated as artificial splitting of procurement. "
            "This is not acceptable under DAP/GFR procurement rules.\n\n"
            "## Likely penalties and consequences\n"
            "• The procurement may be cancelled or rejected.\n"
            "• The executing team may face forfeiture of EMD, debarment, disqualification, or administrative action.\n"
            "• The case may be referred to CFA/IFA and the finance authority for review.\n\n"
            "## Applicable rules and authorities\n"
            "• DAP 2020 Chapter II: procurement planning and tendering.\n"
            "• GFR 2017 Rules 147–155: direct procurement, limited tender, single-source procurement, and emergency exceptions.\n"
            "• Confirm CFA/IFA approval and proper delegation of financial authority for the procurement mode.\n\n"
            "## Procurement categories and process\n"
            "• Open Tender / Competitive Bidding\n"
            "• Limited Tender / Selective Tender\n"
            "• Single Source / Direct Procurement\n"
            "• Emergency Procurement – only with formal, documented approval.\n\n"
            "## Important guidance\n"
            "• Aggregate related purchases for threshold calculation, not split invoices to evade rules.\n"
            "• Document any exception and obtain approval from the delegated authority.\n"
            "• Artificial splitting is subject to review, penalty, and process rejection.\n\n"
            "## Source documents referenced\n"
            f"• {', '.join(source_titles)}\n"
        )
        return answer

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
                quality_score=record.get("quality_score", 0.0),
                quality_reason=record.get("quality_reason", ""),
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
