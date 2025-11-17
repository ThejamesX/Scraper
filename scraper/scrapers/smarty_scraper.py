"""Smarty.cz scraper implementation."""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import time
from urllib.parse import urljoin, quote_plus

from scraper.base_scraper import BaseScraper, Product
from scraper.config import SMARTY_CONFIG, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY


class SmartyScraper(BaseScraper):
    """Scraper for Smarty.cz e-commerce website."""
    
    def __init__(self):
        super().__init__()
        self.config = SMARTY_CONFIG
        self.session = requests.Session()
        self.session.headers.update(self.config['headers'])
    
    def get_website_name(self) -> str:
        return "Smarty.cz"
    
    def search_products(self, query: str, max_results: int = 10) -> List[Product]:
        """Search for products on Smarty.cz"""
        products = []
        
        try:
            # Construct search URL
            search_url = f"{self.config['search_url']}?q={quote_plus(query)}"
            
            # Make request with retry logic
            response = self._make_request(search_url)
            if not response:
                return products
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find product items
            product_items = soup.select(self.config['selectors']['search_results'])
            
            for item in product_items[:max_results]:
                try:
                    product = self._parse_product_item(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    print(f"Error parsing product item: {e}")
                    continue
            
        except Exception as e:
            print(f"Error searching Smarty: {e}")
        
        return products
    
    def get_product_details(self, url: str) -> Optional[Product]:
        """Get detailed product information from Smarty.cz"""
        try:
            response = self._make_request(url)
            if not response:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract product details
            name_elem = soup.select_one('h1.product-title')
            price_elem = soup.select_one(self.config['selectors']['product_price'])
            image_elem = soup.select_one('img.product-detail-image')
            availability_elem = soup.select_one(self.config['selectors']['availability'])
            
            if not name_elem or not price_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            price_text = price_elem.get_text(strip=True)
            price = self.clean_price(price_text)
            currency = self.extract_currency(price_text)
            
            if price is None:
                return None
            
            product = Product(
                name=name,
                price=price,
                currency=currency,
                url=url,
                website=self.website_name,
                image_url=image_elem.get('src') if image_elem else None,
                availability=availability_elem.get_text(strip=True) if availability_elem else None
            )
            
            return product
            
        except Exception as e:
            print(f"Error getting product details from Smarty: {e}")
            return None
    
    def _parse_product_item(self, item) -> Optional[Product]:
        """Parse a single product item from search results."""
        try:
            # Extract product name
            name_elem = item.select_one(self.config['selectors']['product_name'])
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extract price
            price_elem = item.select_one(self.config['selectors']['product_price'])
            if not price_elem:
                return None
            price_text = price_elem.get_text(strip=True)
            price = self.clean_price(price_text)
            
            if price is None:
                return None
            
            # Extract product URL
            link_elem = item.select_one(self.config['selectors']['product_link'])
            if not link_elem:
                return None
            url = urljoin(self.config['base_url'], link_elem.get('href', ''))
            
            # Extract image URL
            image_elem = item.select_one(self.config['selectors']['product_image'])
            image_url = image_elem.get('src') if image_elem else None
            
            # Extract availability
            availability_elem = item.select_one(self.config['selectors']['availability'])
            availability = availability_elem.get_text(strip=True) if availability_elem else None
            
            return Product(
                name=name,
                price=price,
                currency=self.extract_currency(price_text),
                url=url,
                website=self.website_name,
                image_url=image_url,
                availability=availability
            )
            
        except Exception as e:
            print(f"Error parsing product item: {e}")
            return None
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make HTTP request with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    return None
        return None
