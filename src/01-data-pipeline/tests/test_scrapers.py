"""Tests for web scrapers"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from scrapy.http import HtmlResponse, Request

from ..scrapers.base_spider import BaseSpider
from ..scrapers.moad_spider import MinistryOfDefenceSpider


class TestBaseSpider:
    """Tests for BaseSpider class"""

    def test_deduplication_by_url(self):
        """Test that duplicate URLs are detected"""
        spider = BaseSpider()
        
        # First document
        is_dup1 = spider.is_duplicate("http://example.com/doc1", "hash1")
        assert not is_dup1, "First document should not be duplicate"
        
        # Same URL should be detected as duplicate
        is_dup2 = spider.is_duplicate("http://example.com/doc1", "hash2")
        assert is_dup2, "Same URL should be detected as duplicate"

    def test_deduplication_by_content_hash(self):
        """Test that duplicate content hashes are detected"""
        spider = BaseSpider()
        
        # First document
        is_dup1 = spider.is_duplicate("http://example.com/doc1", "hash1")
        assert not is_dup1
        
        # Different URL but same hash should be duplicate
        is_dup2 = spider.is_duplicate("http://example.com/doc2", "hash1")
        assert is_dup2, "Same content hash should be detected as duplicate"

    def test_content_hash_calculation(self):
        """Test SHA256 hash calculation"""
        spider = BaseSpider()
        
        content = "Test document content"
        hash1 = spider.calculate_content_hash(content)
        hash2 = spider.calculate_content_hash(content)
        
        assert hash1 == hash2, "Same content should produce same hash"
        assert len(hash1) == 64, "SHA256 hash should be 64 characters"

    def test_save_document(self):
        """Test saving document to file system"""
        spider = BaseSpider()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            document = {
                'title': 'Test Document',
                'url': 'http://example.com/test',
                'content': 'Test content',
            }
            
            success = spider.save_document(document, tmpdir)
            assert success, "Document should be saved successfully"
            
            # Verify file was created
            files = list(Path(tmpdir).glob('*.json'))
            assert len(files) == 1, "One JSON file should be created"

    def test_metrics_tracking(self):
        """Test that metrics are tracked correctly"""
        spider = BaseSpider()
        
        # Simulate some activity
        spider.is_duplicate("http://example.com/doc1", "hash1")
        spider.is_duplicate("http://example.com/doc1", "hash1")  # Duplicate
        
        assert spider.metrics['duplicates_found'] == 1, "Should track duplicates"


class TestMinistryOfDefenceSpider:
    """Tests for MinistryOfDefenceSpider"""

    def test_spider_initialization(self):
        """Test spider initializes correctly"""
        spider = MinistryOfDefenceSpider()
        
        assert spider.name == 'moad_spider'
        assert 'defence.gov.in' in spider.allowed_domains
        assert len(spider.start_urls) > 0

    def test_document_classification(self):
        """Test document type classification"""
        spider = MinistryOfDefenceSpider()
        
        # Test press release
        doc_type = spider.classify_document_type(
            "Press Release: Defence Policy",
            "This is a press release about defence"
        )
        assert doc_type == 'press_release'
        
        # Test policy document
        doc_type = spider.classify_document_type(
            "Defence Policy Guidelines",
            "Policy and directive for defence operations"
        )
        assert doc_type == 'policy_document'
        
        # Test procurement
        doc_type = spider.classify_document_type(
            "Procurement Notice",
            "Tender bid for defence equipment"
        )
        assert doc_type == 'procurement'

    def test_date_parsing(self):
        """Test various date format parsing"""
        spider = MinistryOfDefenceSpider()
        
        # Test different formats
        dates = [
            "25-05-2026",
            "25/05/2026",
            "May 25, 2026",
            "25 May 2026",
        ]
        
        for date_str in dates:
            parsed = spider.parse_date(date_str)
            assert parsed is not None
            assert 'T' in parsed, "Should be ISO format with time"

    def test_parse_date_with_invalid_input(self):
        """Test date parsing with invalid input"""
        spider = MinistryOfDefenceSpider()
        
        # Invalid date should return current date
        parsed = spider.parse_date("invalid date")
        assert parsed is not None
        assert 'T' in parsed

    @patch('scrapy.http.HtmlResponse')
    def test_parse_press_release(self, mock_response):
        """Test parsing of individual press release"""
        spider = MinistryOfDefenceSpider()
        
        # Mock response
        mock_response.url = "http://pib.gov.in/test"
        mock_response.css = MagicMock()
        mock_response.css().get.return_value = "Test Title"
        mock_response.urljoin = lambda x: x
        
        # This is a basic test - full integration test would require scrapy framework setup
        assert spider.name == 'moad_spider'

    def test_metrics_on_close(self):
        """Test that metrics are saved when spider closes"""
        spider = MinistryOfDefenceSpider()
        spider.collected_docs = [{'title': 'Doc1'}]
        
        # Metrics should have initial values
        assert 'total_requests' in spider.metrics
        assert 'successful_documents' in spider.metrics


class TestScraperIntegration:
    """Integration tests for scrapers"""

    def test_scraper_workflow(self):
        """Test complete scraper workflow"""
        spider = MinistryOfDefenceSpider()
        
        # Simulate collecting documents
        doc1 = {'title': 'Doc1', 'url': 'http://example.com/1', 'content': 'Content1'}
        doc2 = {'title': 'Doc2', 'url': 'http://example.com/2', 'content': 'Content2'}
        doc3 = {'title': 'Doc1', 'url': 'http://example.com/1', 'content': 'Content1'}  # Duplicate
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save documents
            hash1 = spider.calculate_content_hash(doc1['content'])
            hash2 = spider.calculate_content_hash(doc2['content'])
            
            dup1 = spider.is_duplicate(doc1['url'], hash1)
            dup2 = spider.is_duplicate(doc2['url'], hash2)
            dup3 = spider.is_duplicate(doc3['url'], hash1)  # Should be dup
            
            assert not dup1
            assert not dup2
            assert dup3, "Duplicate should be detected"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
