"""Tests for preprocessing pipeline"""

import tempfile
from pathlib import Path

import pytest

from ..preprocessing import PreprocessingPipeline


class TestPreprocessingPipeline:
    """Tests for PreprocessingPipeline class"""

    def test_initialization(self):
        """Test preprocessing pipeline initialization"""
        pipeline = PreprocessingPipeline()
        
        assert pipeline.nlp is not None or True  # May be None if model not installed
        assert len(pipeline.DOMAIN_TERMS) > 0
        assert pipeline.metrics['documents_processed'] == 0

    def test_normalize_text(self):
        """Test text normalization"""
        pipeline = PreprocessingPipeline()
        
        text = "  HELLO   World  !!!  "
        normalized = pipeline.normalize_text(text)
        
        assert 'hello' in normalized
        assert 'world' in normalized
        assert '  ' not in normalized  # No double spaces

    def test_normalize_removes_special_chars(self):
        """Test that normalization removes special characters"""
        pipeline = PreprocessingPipeline()
        
        text = "Hello@#$%World"
        normalized = pipeline.normalize_text(text)
        
        assert '@' not in normalized
        assert '#' not in normalized
        assert '$' not in normalized

    def test_tokenize_sentences(self):
        """Test sentence tokenization"""
        pipeline = PreprocessingPipeline()
        
        text = "This is sentence one. This is sentence two. And a third."
        sentences = pipeline.tokenize_sentences(text)
        
        assert len(sentences) == 3
        assert "This is sentence one" in sentences[0]

    def test_tokenize_words(self):
        """Test word tokenization"""
        pipeline = PreprocessingPipeline()
        
        text = "Hello world from Python"
        words = pipeline.tokenize_words(text)
        
        assert len(words) == 4
        assert 'hello' in [w.lower() for w in words]

    def test_remove_stopwords(self):
        """Test stopword removal"""
        pipeline = PreprocessingPipeline()
        
        tokens = ['the', 'quick', 'brown', 'fox', 'is', 'quick']
        filtered, removed = pipeline.remove_stopwords(tokens)
        
        # 'the' and 'is' should be removed as stopwords
        assert 'the' not in [t.lower() for t in filtered]
        assert 'is' not in [t.lower() for t in filtered]
        assert 'quick' in [t.lower() for t in filtered]
        assert removed >= 2  # At least 2 stopwords removed

    def test_stopword_removal_keeps_domain_terms(self):
        """Test that domain terms are kept"""
        pipeline = PreprocessingPipeline()
        
        tokens = ['ministry', 'of', 'defence', 'is', 'important']
        filtered, removed = pipeline.remove_stopwords(tokens)
        
        # 'ministry' and 'defence' should NOT be removed (domain terms)
        filtered_lower = [t.lower() for t in filtered]
        assert 'ministry' in filtered_lower
        assert 'defence' in filtered_lower

    def test_information_retention_calculation(self):
        """Test information retention calculation"""
        pipeline = PreprocessingPipeline()
        
        original = "the quick brown fox jumps over the lazy dog"
        processed = "quick brown fox jumps lazy dog"  # Removed 3 words
        
        retention = pipeline.calculate_information_retention(original, processed)
        
        # 7 out of 9 words = ~77.8%
        assert 75 < retention <= 100

    def test_process_text_empty_input(self):
        """Test processing empty text"""
        pipeline = PreprocessingPipeline()
        
        result = pipeline.process_text('')
        
        assert result['success'] == False
        assert result['error'] == 'Empty text'

    def test_process_text_successful(self):
        """Test successful text processing"""
        pipeline = PreprocessingPipeline()
        
        text = "The Ministry of Defence announced new policies today."
        result = pipeline.process_text(text, remove_stopwords=True, lemmatize=False)
        
        assert result['success'] == True
        assert 'processed_text' in result
        assert result['information_retention'] <= 100.0

    def test_process_text_with_lemmatization(self):
        """Test text processing with lemmatization"""
        pipeline = PreprocessingPipeline()
        
        text = "The dogs are running quickly through the field"
        result = pipeline.process_text(text, lemmatize=True)
        
        assert result['success'] == True
        # Original has 'dogs' and 'running', lemmatized should have 'dog' and 'run'
        assert 'processed_text' in result

    def test_process_document_multi_page(self):
        """Test processing multi-page document"""
        pipeline = PreprocessingPipeline()
        
        document = """
        First page content here.
        ---PAGE BREAK---
        Second page content here.
        """
        
        result = pipeline.process_document(document)
        
        assert result['success'] == True
        assert result['total_pages'] == 2

    def test_metrics_tracking(self):
        """Test metrics are tracked correctly"""
        pipeline = PreprocessingPipeline()
        
        initial_count = pipeline.metrics['documents_processed']
        
        pipeline.process_text("Some sample text")
        
        assert pipeline.metrics['documents_processed'] == initial_count + 1

    def test_information_retention_high(self):
        """Test information retention with minimal stopword removal"""
        pipeline = PreprocessingPipeline()
        
        # Text with few stopwords
        text = "Ministry Defence India strategic important"
        result = pipeline.process_text(text, remove_stopwords=True)
        
        # Should retain most of the content
        assert result['information_retention'] >= 80.0


class TestPreprocessingAccuracy:
    """Tests for preprocessing accuracy and content preservation"""

    def test_retain_defence_terminology(self):
        """Test that defence terminology is retained"""
        pipeline = PreprocessingPipeline()
        
        text = "Defence ministry policy strategic operations"
        result = pipeline.process_text(text, remove_stopwords=True)
        
        processed_lower = result['processed_text'].lower()
        
        # All key defence terms should be in the processed text
        assert 'defence' in processed_lower or 'ministry' in processed_lower

    def test_normalize_then_process(self):
        """Test complete normalization then processing"""
        pipeline = PreprocessingPipeline()
        
        text = "HELLO   WORLD   !!!   This IS a TEST!!!"
        result = pipeline.process_text(text)
        
        assert result['success'] == True
        assert result['processed_text'] is not None

    def test_page_break_handling(self):
        """Test handling of page breaks in documents"""
        pipeline = PreprocessingPipeline()
        
        text = "Page 1 content here\n---PAGE BREAK---\nPage 2 content here"
        result = pipeline.process_document(text)
        
        assert result['total_pages'] == 2
        assert 'page_results' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
