"""
Base scraper interface for all website scrapers.
Provides abstract base class for implementing website-specific scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    """Product data model."""
    name: str
    price: float
    currency: str
    url: str
    website: str
    image_url: Optional[str] = None
    availability: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    scraped_at: datetime = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()


class BaseScraper(ABC):
    """
    Abstract base class for all website scrapers.
    Enforces consistent interface across different website implementations.
    """
    
    def __init__(self):
        self.website_name = self.get_website_name()
    
    @abstractmethod
    def get_website_name(self) -> str:
        """Return the name of the website this scraper handles."""
        pass
    
    @abstractmethod
    def search_products(self, query: str, max_results: int = 10) -> List[Product]:
        """
        Search for products on the website.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of Product objects
        """
        pass
    
    @abstractmethod
    def get_product_details(self, url: str) -> Optional[Product]:
        """
        Get detailed information about a specific product.
        
        Args:
            url: Product URL
            
        Returns:
            Product object or None if not found
        """
        pass
    
    def clean_price(self, price_text: str) -> Optional[float]:
        """
        Extract numeric price from text.
        
        Args:
            price_text: Raw price text (e.g., "$123.45", "123,45 €")
            
        Returns:
            Float price or None if parsing fails
        """
        if not price_text:
            return None
        
        # Remove common currency symbols and whitespace
        cleaned = price_text.strip()
        for symbol in ['$', '€', '£', 'zł', 'Kč', 'CZK', 'PLN']:
            cleaned = cleaned.replace(symbol, '')
        
        cleaned = cleaned.replace(' ', '')
        
        # Determine if comma or dot is decimal separator
        # If both are present, the last one is the decimal separator
        if ',' in cleaned and '.' in cleaned:
            # Both present: last one is decimal separator
            if cleaned.rfind(',') > cleaned.rfind('.'):
                # Comma is decimal: 1.234,56 -> remove dots, replace comma
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                # Dot is decimal: 1,234.56 -> remove commas
                cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            # Only comma: could be decimal or thousand separator
            # If only one comma and 2 digits after it, it's decimal
            comma_count = cleaned.count(',')
            if comma_count == 1 and len(cleaned.split(',')[1]) == 2:
                cleaned = cleaned.replace(',', '.')
            else:
                # Otherwise remove it as thousand separator
                cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    def extract_currency(self, price_text: str) -> str:
        """
        Extract currency from price text.
        
        Args:
            price_text: Raw price text
            
        Returns:
            Currency code (default: USD)
        """
        currency_map = {
            '$': 'USD',
            '€': 'EUR',
            '£': 'GBP',
            'zł': 'PLN',
            'Kč': 'CZK',
            'CZK': 'CZK',
            'PLN': 'PLN'
        }
        
        for symbol, code in currency_map.items():
            if symbol in price_text:
                return code
        
        return 'USD'
