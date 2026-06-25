"""Text preprocessing pipeline for normalizing extracted text"""

import logging
import re
from typing import Dict, List, Optional

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class PreprocessingPipeline:
    """
    Text preprocessing pipeline for normalizing OCR output.
    
    Steps:
    1. Text normalization (lowercase, spacing, special chars)
    2. Tokenization (sentence and word level)
    3. Stopword removal (keeping domain terms)
    4. Lemmatization
    5. Information retention measurement
    """

    # Defence-specific terms to keep (not remove as stopwords)
    DOMAIN_TERMS = {
        'defence', 'defense', 'military', 'army', 'navy', 'air force',
        'security', 'strategic', 'operational', 'combat', 'weapons',
        'procurement', 'budget', 'policy', 'authority', 'ministry',
        'parliament', 'lok sabha', 'rajya sabha', 'pib', 'drdo',
        'india', 'indian', 'national', 'government', 'state',
        'ministry', 'department', 'agency', 'commission',
    }

    def __init__(self, language: str = 'en'):
        """
        Initialize preprocessing pipeline.
        
        Args:
            language: Language code (en, hi)
        """
        self.logger = logging.getLogger(__name__)
        
        try:
            if language == 'en':
                self.nlp = spacy.load('en_core_web_sm')
            else:
                self.nlp = spacy.load('en_core_web_sm')  # Fallback to English
                self.logger.warning(f"Language {language} not available, using English")
        except OSError:
            self.logger.error("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.stop_words = set(stopwords.words('english')) - self.DOMAIN_TERMS
        self.metrics = {
            'documents_processed': 0,
            'total_tokens': 0,
            'total_stopwords_removed': 0,
            'information_retention': 100.0,
        }

    def normalize_text(self, text: str) -> str:
        """
        Normalize text (lowercase, spacing, special chars).
        
        Args:
            text: Raw text
            
        Returns:
            Normalized text
        """
        if not text:
            return ''
        
        # Lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep common punctuation
        text = re.sub(r'[^\w\s\.\,\?\!\-\(\)\:]', '', text)
        
        # Remove extra dots and spaces
        text = re.sub(r'\.+', '.', text)
        text = text.strip()
        
        return text

    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of sentences
        """
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            self.logger.error(f"Error tokenizing sentences: {e}")
            return [text]

    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of words
        """
        try:
            tokens = word_tokenize(text)
            return [t.strip() for t in tokens if t.strip()]
        except Exception as e:
            self.logger.error(f"Error tokenizing words: {e}")
            return text.split()

    def remove_stopwords(self, tokens: List[str]) -> tuple:
        """
        Remove stopwords from token list.
        
        Args:
            tokens: List of word tokens
            
        Returns:
            Tuple of (filtered_tokens, num_removed)
        """
        removed = 0
        filtered = []
        
        for token in tokens:
            if token.lower() in self.stop_words:
                removed += 1
            else:
                filtered.append(token)
        
        self.metrics['total_stopwords_removed'] += removed
        return filtered, removed

    def lemmatize(self, text: str) -> str:
        """
        Lemmatize text using spaCy.
        
        Args:
            text: Text to lemmatize
            
        Returns:
            Lemmatized text
        """
        if not self.nlp:
            self.logger.warning("spaCy model not loaded, skipping lemmatization")
            return text
        
        try:
            doc = self.nlp(text)
            lemmatized = ' '.join([token.lemma_ for token in doc])
            return lemmatized
        except Exception as e:
            self.logger.error(f"Error lemmatizing: {e}")
            return text

    def calculate_information_retention(self, original: str, processed: str) -> float:
        """
        Calculate information retention percentage.
        
        Args:
            original: Original text
            processed: Processed text
            
        Returns:
            Retention percentage (0-100)
        """
        if not original:
            return 100.0
        
        original_len = len(original.split())
        processed_len = len(processed.split())
        
        retention = (processed_len / original_len) * 100
        return min(retention, 100.0)  # Cap at 100%

    def process_text(
        self,
        text: str,
        remove_stopwords: bool = True,
        lemmatize: bool = True,
        keep_sentences: bool = False
    ) -> Dict:
        """
        Process text through full pipeline.
        
        Args:
            text: Raw text to process
            remove_stopwords: Whether to remove stopwords
            lemmatize: Whether to lemmatize
            keep_sentences: Whether to keep sentence structure
            
        Returns:
            Dictionary with processing results
        """
        self.metrics['documents_processed'] += 1
        
        if not text:
            return {
                'success': False,
                'error': 'Empty text',
                'processed_text': '',
                'information_retention': 100.0,
            }
        
        # Step 1: Normalize
        normalized = self.normalize_text(text)
        
        # Step 2: Tokenize (sentences if requested)
        if keep_sentences:
            sentences = self.tokenize_sentences(normalized)
            processed_parts = []
            
            for sentence in sentences:
                tokens = self.tokenize_words(sentence)
                
                if remove_stopwords:
                    tokens, _ = self.remove_stopwords(tokens)
                
                processed_parts.append(' '.join(tokens))
            
            processed = '\n'.join(processed_parts)
        else:
            # Simple word tokenization
            tokens = self.tokenize_words(normalized)
            self.metrics['total_tokens'] += len(tokens)
            
            if remove_stopwords:
                tokens, _ = self.remove_stopwords(tokens)
            
            processed = ' '.join(tokens)
        
        # Step 3: Lemmatize (optional)
        if lemmatize:
            processed = self.lemmatize(processed)
        
        # Step 4: Calculate retention
        retention = self.calculate_information_retention(text, processed)
        self.metrics['information_retention'] = retention
        
        return {
            'success': True,
            'original_text': text,
            'processed_text': processed,
            'original_length': len(text),
            'processed_length': len(processed),
            'information_retention': round(retention, 2),
        }

    def process_document(self, document_text: str) -> Dict:
        """
        Process a complete document (possibly multi-page).
        
        Args:
            document_text: Full document text
            
        Returns:
            Dictionary with processing results
        """
        # Split by page breaks (if they exist)
        pages = document_text.split('---PAGE BREAK---')
        
        processed_pages = []
        total_retention = 0
        
        for page in pages:
            result = self.process_text(
                page.strip(),
                remove_stopwords=True,
                lemmatize=True,
                keep_sentences=True
            )
            processed_pages.append(result)
            total_retention += result['information_retention']
        
        avg_retention = total_retention / len(processed_pages) if processed_pages else 100.0
        
        return {
            'success': True,
            'total_pages': len(processed_pages),
            'page_results': processed_pages,
            'average_information_retention': round(avg_retention, 2),
        }

    def get_metrics(self) -> Dict:
        """Get current processing metrics."""
        return self.metrics


# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    pipeline = PreprocessingPipeline()
    
    # Example text
    sample_text = """
    MINISTRY OF DEFENCE PRESS RELEASE
    The Government of India has approved new defence policy guidelines
    for strategic procurement and operational efficiency.
    All stakeholders must follow the procedures outlined herein.
    """
    
    result = pipeline.process_text(sample_text)
    print(f"Original: {result['original_text'][:100]}...")
    print(f"Processed: {result['processed_text'][:100]}...")
    print(f"Retention: {result['information_retention']}%")
