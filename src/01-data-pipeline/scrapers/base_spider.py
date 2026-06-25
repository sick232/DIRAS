"""Base spider class with common functionality for all scrapers"""

import hashlib
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import scrapy
from scrapy.http import HtmlResponse


class BaseSpider(scrapy.Spider, ABC):
    """
    Base spider class for all DIRAS document scrapers.
    
    Provides common functionality:
    - Deduplication (URL + content hash)
    - Metadata extraction
    - Error handling
    - Metrics tracking
    """

    # Settings
    allowed_domains: List[str] = []
    start_urls: List[str] = []
    name: str = "base_spider"
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,  # 1 second delay between requests
        'CONCURRENT_REQUESTS': 4,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'COOKIES_ENABLED': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collected_docs = []
        self.seen_urls = set()
        self.seen_hashes = set()
        self.errors = []
        self.metrics = {
            'total_requests': 0,
            'successful_documents': 0,
            'duplicates_found': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat(),
        }
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def parse_document_page(self, response: HtmlResponse) -> Dict:
        """
        Parse a document page and extract metadata.
        Must be implemented by subclasses.
        
        Args:
            response: Scrapy response object
            
        Returns:
            Dictionary with document metadata (title, url, date, content, etc.)
        """
        pass

    def is_duplicate(self, url: str, content_hash: str) -> bool:
        """
        Check if document is already collected (by URL or content hash).
        
        Args:
            url: Document URL
            content_hash: SHA256 hash of document content
            
        Returns:
            True if duplicate, False otherwise
        """
        if url in self.seen_urls or content_hash in self.seen_hashes:
            self.metrics['duplicates_found'] += 1
            return True
        
        self.seen_urls.add(url)
        self.seen_hashes.add(content_hash)
        return False

    def extract_document_url(self, response: HtmlResponse) -> Optional[str]:
        """
        Extract actual document URL (PDF/DOC) from response.
        Override in subclasses for specific extraction logic.
        
        Args:
            response: Scrapy response object
            
        Returns:
            Document URL or None if not found
        """
        # Try to find PDF/DOC links
        links = response.css('a[href$=".pdf"]::attr(href), a[href$=".doc"]::attr(href), a[href$=".docx"]::attr(href)').getall()
        if links:
            return urljoin(response.url, links[0])
        return None

    def extract_metadata(self, response: HtmlResponse) -> Dict:
        """
        Extract document metadata (title, date, etc.).
        Override in subclasses for specific extraction logic.
        
        Args:
            response: Scrapy response object
            
        Returns:
            Dictionary with metadata
        """
        return {
            'title': response.css('title::text').get('').strip(),
            'url': response.url,
            'date_scraped': datetime.now().isoformat(),
            'domain': urlparse(response.url).netloc,
        }

    def calculate_content_hash(self, content: str) -> str:
        """
        Calculate SHA256 hash of content for deduplication.
        
        Args:
            content: Document content
            
        Returns:
            SHA256 hash (hex)
        """
        return hashlib.sha256(content.encode()).hexdigest()

    def save_document(self, document: Dict, output_dir: str = 'data/raw') -> bool:
        """
        Save document to file system.
        
        Args:
            document: Document dictionary
            output_dir: Directory to save to
            
        Returns:
            True if saved successfully
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create unique filename from URL hash
            url_hash = self.calculate_content_hash(document.get('url', ''))
            filename = f"{self.name}_{url_hash[:8]}.json"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(document, f, indent=2, ensure_ascii=False)
            
            self.metrics['successful_documents'] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving document: {e}")
            self.errors.append(str(e))
            self.metrics['errors'] += 1
            return False

    def save_metrics(self, output_file: str = 'data/processed/scraper_metrics.json'):
        """Save metrics to file."""
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.metrics['end_time'] = datetime.now().isoformat()
            self.metrics['documents_collected'] = len(self.collected_docs)
            self.metrics['duplicates_skipped'] = self.metrics['duplicates_found']
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2)
                
            self.logger.info(f"Metrics saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving metrics: {e}")

    def closed(self, reason: str):
        """Spider closed callback."""
        self.logger.info(f"Spider closed: {reason}")
        self.logger.info(f"Collected: {self.metrics['successful_documents']} documents")
        self.logger.info(f"Duplicates: {self.metrics['duplicates_found']}")
        self.logger.info(f"Errors: {self.metrics['errors']}")
        self.save_metrics()
