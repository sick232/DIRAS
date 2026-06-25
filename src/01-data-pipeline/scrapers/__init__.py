"""Web scrapers for collecting defence documents"""

from .base_spider import BaseSpider
from .moad_spider import MinistryOfDefenceSpider

__all__ = ["BaseSpider", "MinistryOfDefenceSpider"]
