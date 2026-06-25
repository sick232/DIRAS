"""
Google Gemini LLM Integration with Retry Logic
Wrapper around Google's Gemini API for generating answers based on document context
"""

import logging
import time
from typing import Optional
import os
from datetime import datetime
import warnings

try:
    import google.genai as genai
except ImportError:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai
    except ImportError:
        raise ImportError("Please install google-genai: pip install google-genai")

from src.shared.config import settings

logger = logging.getLogger(__name__)

# Module-level caching for Gemini client instance
_gemini_instance = None
_cached_api_key = None


class GeminiClient:
    """
    Client for Google Gemini API with retry logic and error handling
    Uses google-generativeai SDK
    """

    def __init__(self, api_key: str):
        """
        Initialize Gemini client with validation

        Args:
            api_key: Google API key from console.cloud.google.com
            
        Raises:
            ValueError: If API key is invalid or empty
        """
        if not api_key or not api_key.strip():
            raise ValueError("Gemini API key is required and cannot be empty")
        
        self.api_key = api_key
        self.model = settings.gemini_model
        self.max_retries = settings.llm_max_retries
        self.retry_delay = settings.llm_retry_delay
        self.retry_backoff = settings.llm_retry_backoff
        self.request_timeout = settings.llm_request_timeout
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Get model
        self.client = genai.GenerativeModel(self.model)
        
        # Validate API key at initialization if enabled
        if settings.llm_api_validation_enabled:
            self._validate_api_key()
        
        logger.info(f"Gemini client initialized (model={self.model}, retries={self.max_retries})")
    
    def _validate_api_key(self) -> bool:
        """
        Validate API key by making a test request
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            logger.info("Validating Gemini API key...")
            response = self.client.generate_content("test", stream=False)
            logger.info("✓ Gemini API key validated successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠ Gemini API key validation failed: {str(e)}")
            return False
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if error is retryable
        
        Args:
            error: Exception to check
            
        Returns:
            bool: True if error should trigger retry
        """
        error_str = str(error).lower()
        
        # Check for transient issues
        transient_keywords = ['timeout', 'connection', 'temporarily', 'unavailable', 'rate limit', 'service unavailable', 'overloaded']
        if any(keyword in error_str for keyword in transient_keywords):
            return True
        
        return False
    
    def _parse_error(self, error: Exception) -> dict:
        """
        Parse error and determine type
        
        Args:
            error: Exception to parse
            
        Returns:
            dict with error details
        """
        error_str = str(error)
        
        if "401" in error_str or "Unauthorized" in error_str or "API key" in error_str or "invalid_api_key" in error_str:
            return {
                "type": "auth_error",
                "message": "Invalid API key",
                "retryable": False
            }
        elif "403" in error_str or "Forbidden" in error_str or "permission" in error_str.lower():
            return {
                "type": "permission_error",
                "message": "API access forbidden",
                "retryable": False
            }
        elif "429" in error_str or "rate" in error_str.lower() or "quota" in error_str.lower():
            return {
                "type": "rate_limit",
                "message": "API rate limit exceeded",
                "retryable": True
            }
        elif "timeout" in error_str.lower() or "deadline" in error_str.lower():
            return {
                "type": "timeout",
                "message": "Request timeout",
                "retryable": True
            }
        elif "overloaded" in error_str.lower() or "temporarily" in error_str.lower():
            return {
                "type": "service_unavailable",
                "message": "Service temporarily unavailable",
                "retryable": True
            }
        else:
            return {
                "type": "unknown",
                "message": str(error),
                "retryable": False
            }

    def generate_answer(
        self,
        query: str,
        context: str,
        temperature: float = None,
        max_tokens: int = 1024
        ,
        raw_prompt: Optional[str] = None
    ) -> dict:
        """
        Generate an answer using Gemini LLM with automatic retry

        Args:
            query: User's question
            context: Retrieved document context to answer from
            temperature: Creativity level (0.0-2.0), lower = more factual
            max_tokens: Maximum tokens in response

        Returns:
            dict with keys:
                - answer: Generated text answer
                - confidence: Confidence score (0-1)
                - model: Model name used
                - tokens_used: Number of tokens used (estimated)
                - error: Error message if failed
        """
        
        if temperature is None:
            temperature = settings.gemini_temperature
        
        if raw_prompt:
            system_prompt = "You are a helpful assistant for Defence Intelligence Retrieval and Analysis System (DIRAS)."
            user_prompt = raw_prompt
        else:
            # System prompt enforces grounding in documents
            system_prompt = """You are a helpful assistant for Defence Intelligence Retrieval and Analysis System (DIRAS).
    Answer questions ONLY based on the provided official documents.
    If information is not found in the documents, say so clearly.
    Be concise and factual. Do not speculate beyond what's in the documents.
    Always cite which document your answer comes from."""

            # User prompt with context
            user_prompt = f"""Based on these official documents, answer the following question:

    DOCUMENTS:
    {context}

    QUESTION: {query}

    Answer:"""

        # Retry loop with exponential backoff
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Gemini API call (attempt {attempt + 1}/{self.max_retries}) for query: {query[:50]}...")

                # Call Gemini API
                response = self.client.generate_content(
                    user_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_NONE"
                        },
                    ],
                    stream=False
                )

                # Extract answer
                answer = response.text if response and response.text else ""
                
                if not answer:
                    raise ValueError("Empty response from Gemini API")
                
                # Estimate tokens (roughly 0.75 tokens per word)
                tokens_used = int(len(answer.split()) / 0.75)

                # Calculate confidence based on response length and model
                confidence = min(1.0, len(answer.split()) / 50)  # 50 words = 100% confidence
                confidence = max(0.85, confidence)  # Minimum 85% confidence for Gemini

                logger.info(f"✓ Gemini API response successful (tokens: ~{tokens_used})")

                return {
                    "answer": answer,
                    "confidence": confidence,
                    "model": self.model,
                    "tokens_used": tokens_used,
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": None
                }

            except Exception as e:
                error_info = self._parse_error(e)
                
                logger.warning(f"⚠ Attempt {attempt + 1} failed: {error_info['type']} - {error_info['message']}")
                
                # If not retryable or last attempt, return error
                if not error_info['retryable'] or attempt == self.max_retries - 1:
                    logger.error(f"✗ Gemini API call failed: {error_info['message']}")
                    return {
                        "answer": "",
                        "confidence": 0.0,
                        "model": self.model,
                        "tokens_used": 0,
                        "timestamp": datetime.utcnow().isoformat(),
                        "error": error_info['message'],
                        "error_type": error_info['type']
                    }
                
                # Calculate backoff delay
                delay = self.retry_delay * (self.retry_backoff ** attempt)
                logger.info(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)

    def is_available(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            response = self.client.generate_content("test", stream=False)
            return response and response.text
        except Exception as e:
            logger.warning(f"Gemini API not available: {e}")
            return False


def get_gemini_client(api_key: Optional[str] = None) -> GeminiClient:
    """
    Get or create Gemini client instance
    
    Args:
        api_key: Google API key (uses GEMINI_API_KEY env var if not provided)
    
    Returns:
        GeminiClient instance
    """
    global _gemini_instance
    global _cached_api_key
    
    # Use provided api_key, or get from environment
    key = api_key or os.getenv("GEMINI_API_KEY")
    
    if not key:
        raise ValueError("GEMINI_API_KEY not provided and not found in environment")
    
    # Recreate instance if api_key has changed or first time
    if _gemini_instance is None or _cached_api_key != key:
        _gemini_instance = GeminiClient(key)
        _cached_api_key = key
    
    return _gemini_instance
