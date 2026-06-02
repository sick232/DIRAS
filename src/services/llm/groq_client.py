"""
Groq LLM Client for RAG pipeline
Uses Groq API (OpenAI-compatible) with retry logic and error handling
"""

import os
import logging
import time
from typing import Optional
from openai import OpenAI, RateLimitError, APIError, APIConnectionError, APITimeoutError
from src.shared.config import settings

logger = logging.getLogger(__name__)

# Global instance
_groq_instance: Optional['GroqClient'] = None
_cached_api_key: Optional[str] = None


class GroqClient:
    """Groq LLM client wrapper with retry logic and error handling"""
    
    def __init__(self, api_key: str):
        """
        Initialize Groq client with validation
        
        Args:
            api_key: Groq API key
            
        Raises:
            ValueError: If API key is invalid or empty
        """
        if not api_key or not api_key.strip():
            raise ValueError("Groq API key is required and cannot be empty")
        
        self.api_key = api_key
        self.model = settings.groq_model
        self.max_retries = settings.llm_max_retries
        self.retry_delay = settings.llm_retry_delay
        self.retry_backoff = settings.llm_retry_backoff
        self.request_timeout = settings.llm_request_timeout
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=self.request_timeout
        )
        
        # Validate API key at initialization if enabled
        if settings.llm_api_validation_enabled:
            self._validate_api_key()
        
        logger.info(f"Groq client initialized (model={self.model}, retries={self.max_retries})")
    
    def _validate_api_key(self) -> bool:
        """
        Validate API key by making a test request
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            logger.info("Validating Groq API key...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                temperature=0.3
            )
            logger.info("✓ Groq API key validated successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠ Groq API key validation failed: {str(e)}")
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
        Generate answer using Groq with automatic retry
        
        Args:
            query: User query
            context: Retrieved document context
            temperature: Temperature for generation (uses config default if None)
            max_tokens: Max tokens in response
            
        Returns:
            dict with answer and metadata
        """
        if temperature is None:
            temperature = settings.grok_temperature
        
        system_prompt = """You are an expert defence analyst assistant. 
Use the provided context to answer questions accurately.
Keep responses concise and well-structured.
If information is not in the context, say so clearly."""
        
        user_message = f"""Context from defence documents:

{context}

Question: {query}

Please provide a clear, detailed answer based on the context above."""
        
        last_error = None
        
        # Retry loop with exponential backoff
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Groq API call (attempt {attempt + 1}/{self.max_retries}) for query: {query[:50]}...")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.request_timeout
                )
                
                answer = response.choices[0].message.content
                tokens_used = response.usage.total_tokens if response.usage else 0
                
                logger.info(f"✓ Groq API call successful (tokens: {tokens_used})")
                
                return {
                    "answer": answer,
                    "model": self.model,
                    "stop_reason": response.choices[0].finish_reason,
                    "tokens_used": tokens_used,
                    "confidence": 0.95,
                    "error": None
                }
                
            except Exception as e:
                last_error = e
                error_info = self._parse_error(e)
                
                logger.warning(f"⚠ Attempt {attempt + 1} failed: {error_info['type']} - {error_info['message']}")
                
                # If not retryable or last attempt, return error
                if not error_info['retryable'] or attempt == self.max_retries - 1:
                    logger.error(f"✗ Groq API call failed: {error_info['message']}")
                    return {
                        "error": error_info['message'],
                        "answer": None,
                        "model": self.model,
                        "tokens_used": 0,
                        "confidence": 0.0,
                        "error_type": error_info['type']
                    }
                
                # Calculate backoff delay
                delay = self.retry_delay * (self.retry_backoff ** attempt)
                logger.info(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)


def get_groq_client(api_key: Optional[str] = None) -> GroqClient:
    """
    Get or create Groq client instance
    
    Args:
        api_key: Groq API key (uses GROQ_API_KEY env var if not provided)
    
    Returns:
        GroqClient instance
    """
    global _groq_instance
    global _cached_api_key
    
    # Use provided api_key, or get from environment
    key = api_key or os.getenv("GROQ_API_KEY")
    
    if not key:
        raise ValueError("GROQ_API_KEY not provided and not found in environment")
    
    # Recreate instance if api_key has changed or first time
    if _groq_instance is None or _cached_api_key != key:
        _groq_instance = GroqClient(key)
        _cached_api_key = key
    
    return _groq_instance
