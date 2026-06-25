"""Ministry of Defence (MoD) spider for scraping defence documents"""

import re
from datetime import datetime
from typing import Dict, Optional

from scrapy.http import HtmlResponse

from .base_spider import BaseSpider


class MinistryOfDefenceSpider(BaseSpider):
    """
    Spider for collecting documents from Ministry of Defence India website.
    
    Targets:
    - Press releases
    - Announcements
    - Policy documents
    - Parliamentary reports
    
    Target: Collect 5,000+ documents in first phase
    """

    name = 'moad_spider'
    allowed_domains = ['defence.gov.in', 'pib.gov.in']
    
    # Starting URLs for scraping
    start_urls = [
        'https://pib.gov.in/PressReleasePage.aspx?PRID=1',  # PIB Press Releases
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,  # 2 second delay (defence websites may be sensitive)
        'CONCURRENT_REQUESTS': 2,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'COOKIES_ENABLED': False,
    }

    def start_requests(self):
        """Generate initial requests for each URL."""
        for url in self.start_urls:
            self.logger.info(f"Starting scrape from {url}")
            yield scrapy.Request(url, callback=self.parse, dont_obey_robotstxt=False)

    def parse(self, response: HtmlResponse):
        """
        Parse press release listing page and extract document links.
        
        Args:
            response: Scrapy response object
        """
        self.metrics['total_requests'] += 1
        
        # Extract all press release links from the page
        press_release_links = response.css('a.pibpress-link::attr(href)').getall()
        
        if not press_release_links:
            # Fallback: Try to find all links that might be press releases
            press_release_links = response.css('a[href*="PRID"]::attr(href)').getall()
        
        self.logger.info(f"Found {len(press_release_links)} press release links on {response.url}")
        
        # Follow each press release link to detail page
        for link in press_release_links[:100]:  # Limit to 100 per page for testing
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_press_release, dont_obey_robotstxt=False)
        
        # Try to find next page link
        next_page = response.css('a:contains("Next")::attr(href)').get()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse, dont_obey_robotstxt=False)

    def parse_press_release(self, response: HtmlResponse) -> Dict:
        """
        Parse individual press release page and extract document details.
        
        Args:
            response: Scrapy response object
            
        Yields:
            Document dictionaries
        """
        self.metrics['total_requests'] += 1
        
        try:
            # Extract title
            title = response.css('h1::text').get('')
            if not title:
                title = response.css('.pibpress-title::text').get('')
            
            title = title.strip()
            
            # Extract date
            date_text = response.css('.pibpress-date::text, .date::text').get('')
            date_published = self.parse_date(date_text)
            
            # Extract document content
            content = response.css('.pibpress-content::text, .content::text').getall()
            content_text = ' '.join([c.strip() for c in content if c.strip()])
            
            # Extract ministry/department
            ministry = response.css('.pibpress-ministry::text, .ministry::text').get('Ministry of Defence')
            ministry = ministry.strip()
            
            # Calculate content hash for deduplication
            content_hash = self.calculate_content_hash(content_text)
            
            # Check for duplicates
            if self.is_duplicate(response.url, content_hash):
                self.logger.debug(f"Skipping duplicate: {title}")
                return
            
            # Try to extract PDF/document link
            pdf_link = response.css('a[href$=".pdf"]::attr(href)').get()
            if pdf_link:
                pdf_link = response.urljoin(pdf_link)
            
            # Build document dictionary
            document = {
                'title': title,
                'url': response.url,
                'content': content_text[:5000],  # Limit to first 5000 chars
                'date_published': date_published,
                'ministry': ministry,
                'content_hash': content_hash,
                'source': 'Ministry of Defence (PIB)',
                'document_type': self.classify_document_type(title, content_text),
                'metadata': {
                    'domain': 'pib.gov.in',
                    'page_title': response.css('title::text').get(''),
                    'language': 'en',
                }
            }
            
            # Save and track document
            self.collected_docs.append(document)
            self.save_document(document)
            
            self.logger.info(f"Collected: {title} ({len(self.collected_docs)} total)")
            
            yield document
            
        except Exception as e:
            self.logger.error(f"Error parsing press release {response.url}: {e}")
            self.errors.append(str(e))
            self.metrics['errors'] += 1

    def parse_date(self, date_text: str) -> str:
        """
        Parse various date formats found on websites.
        
        Args:
            date_text: Raw date text from website
            
        Returns:
            ISO format date string
        """
        if not date_text:
            return datetime.now().isoformat()
        
        date_text = date_text.strip()
        
        # Try common date formats
        formats = [
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%B %d, %Y',
            '%d %B %Y',
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_text, fmt)
                return parsed.isoformat()
            except ValueError:
                continue
        
        # If parsing fails, return current date
        self.logger.warning(f"Could not parse date: {date_text}")
        return datetime.now().isoformat()

    def classify_document_type(self, title: str, content: str) -> str:
        """
        Classify document type based on title and content.
        
        Args:
            title: Document title
            content: Document content
            
        Returns:
            Document type classification
        """
        text = (title + ' ' + content).lower()
        
        if any(word in text for word in ['press release', 'statement', 'announcement']):
            return 'press_release'
        elif any(word in text for word in ['policy', 'directive', 'guidelines']):
            return 'policy_document'
        elif any(word in text for word in ['procurement', 'tender', 'bid']):
            return 'procurement'
        elif any(word in text for word in ['financial', 'budget', 'expenditure']):
            return 'financial_report'
        elif any(word in text for word in ['parliamentary', 'lok sabha', 'rajya sabha']):
            return 'parliamentary_report'
        else:
            return 'general_document'


# For running spider directly
if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })
    
    process.crawl(MinistryOfDefenceSpider)
    process.start()
