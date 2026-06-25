"""
Grok LLM Integration with Retry Logic
Wrapper around xAI Grok API for generating answers based on document context
"""

import logging
import time
from typing import Optional
import os
from datetime import datetime

# Using OpenAI client which is compatible with xAI Grok API
try:
    from openai import OpenAI, RateLimitError, APIError, APIConnectionError, APITimeoutError
except ImportError:
    raise ImportError("Please install openai: pip install openai")

from src.shared.config import settings

logger = logging.getLogger(__name__)

# Module-level caching for Grok client instance
_grok_instance = None
_cached_api_key = None


class GrokClient:
    """
    Client for xAI Grok API with retry logic and error handling
    Uses OpenAI-compatible endpoint for Grok
    """

    def __init__(self, api_key: str):
        """
        Initialize Grok client with validation

        Args:
            api_key: xAI API key from console.x.ai
            
        Raises:
            ValueError: If API key is invalid or empty
        """
        if not api_key or not api_key.strip():
            raise ValueError("Grok API key is required and cannot be empty")
        
        self.api_key = api_key
        self.model = settings.grok_model
        self.max_retries = settings.llm_max_retries
        self.retry_delay = settings.llm_retry_delay
        self.retry_backoff = settings.llm_retry_backoff
        self.request_timeout = settings.llm_request_timeout
        
        # Initialize OpenAI client with xAI endpoint
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
            timeout=self.request_timeout
        )
        
        # Validate API key at initialization if enabled
        if settings.llm_api_validation_enabled:
            self._validate_api_key()
        
        logger.info(f"Grok client initialized (model={self.model}, retries={self.max_retries})")
    
    def _validate_api_key(self) -> bool:
        """
        Validate API key by making a test request
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            logger.info("Validating Grok API key...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                temperature=0.3
            )
            logger.info("✓ Grok API key validated successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠ Grok API key validation failed: {str(e)}")
            return False
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if error is retryable
        
        Args:
            error: Exception to check
            
        Returns:
            bool: True if error should trigger retry
        """
        # Retryable errors
        if isinstance(error, (RateLimitError, APIConnectionError, APITimeoutError)):
            return True
        
        # Check error message for transient issues
        error_str = str(error).lower()
        transient_keywords = ['timeout', 'connection', 'temporarily', 'unavailable', 'rate limit']
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
        
        if isinstance(error, RateLimitError):
            return {
                "type": "rate_limit",
                "message": "API rate limit exceeded",
                "retryable": True
            }
        elif isinstance(error, APITimeoutError):
            return {
                "type": "timeout",
                "message": "Request timeout",
                "retryable": True
            }
        elif isinstance(error, APIConnectionError):
            return {
                "type": "connection",
                "message": "Connection error",
                "retryable": True
            }
        elif "401" in error_str or "Unauthorized" in error_str:
            return {
                "type": "auth_error",
                "message": "Invalid API key",
                "retryable": False
            }
        elif "403" in error_str or "Forbidden" in error_str:
            return {
                "type": "permission_error",
                "message": "API access forbidden",
                "retryable": False
            }
        elif "400" in error_str:
            return {
                "type": "bad_request",
                "message": "Invalid request parameters",
                "retryable": False
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
    ) -> dict:
        """
        Generate an answer using Grok LLM with automatic retry

        Args:
            query: User's question
            context: Retrieved document context to answer from
            temperature: Creativity level (0.0-1.0), lower = more factual
            max_tokens: Maximum tokens in response

        Returns:
            dict with keys:
                - answer: Generated text answer
                - confidence: Confidence score (0-1)
                - model: Model name used
                - tokens_used: Number of tokens used
                - error: Error message if failed
        """
        
        if temperature is None:
            temperature = settings.grok_temperature
        
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
                logger.info(f"Grok API call (attempt {attempt + 1}/{self.max_retries}) for query: {query[:50]}...")

                # Call Grok API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.request_timeout
                )

                # Extract answer
                answer = response.choices[0].message.content
                tokens_used = response.usage.total_tokens if response.usage else 0

                # Calculate confidence based on response length and model
                confidence = min(1.0, len(answer.split()) / 50)  # 50 words = 100% confidence
                confidence = max(0.5, confidence)  # Minimum 50% confidence

                logger.info(f"✓ Grok API response successful (tokens: {tokens_used})")

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
                    logger.error(f"✗ Grok API call failed: {error_info['message']}")
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
        """Check if Grok API is accessible"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10,
                timeout=self.request_timeout
            )
            return True
        except Exception as e:
            logger.warning(f"Grok API not available: {e}")
            return False


def get_grok_client(api_key: Optional[str] = None) -> GrokClient:
    """
    Get or create Grok client instance

    Args:
        api_key: xAI API key (uses GROK_API_KEY env var if not provided)

    Returns:
        GrokClient instance
    """
    global _grok_instance
    global _cached_api_key
    
    # Use provided api_key, or get from environment
    key = api_key or os.getenv("GROK_API_KEY")
    
    if not key:
        raise ValueError("GROK_API_KEY not provided and not found in environment")
    
    # Recreate instance if api_key has changed or first time
    if _grok_instance is None or _cached_api_key != key:
        _grok_instance = GrokClient(key)
        _cached_api_key = key
    
    return _grok_instance
