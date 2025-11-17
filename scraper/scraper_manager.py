"""Unified scraper manager for all websites."""

from typing import List, Dict
from scraper.base_scraper import Product
from scraper.scrapers import AlzaScraper, AllegroScraper, SmartyScraper
from scraper.models import Database


class ScraperManager:
    """
    Manager class for coordinating multiple scrapers.
    Provides a unified interface for searching products across all websites.
    """
    
    def __init__(self, db_path: str = 'price_tracker.db'):
        """
        Initialize scraper manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.scrapers = {
            'alza': AlzaScraper(),
            'allegro': AllegroScraper(),
            'smarty': SmartyScraper()
        }
        self.db = Database(db_path)
    
    def search_all(self, query: str, max_results_per_site: int = 10) -> Dict[str, List[Product]]:
        """
        Search for products across all websites.
        
        Args:
            query: Search query
            max_results_per_site: Maximum results per website
            
        Returns:
            Dictionary mapping website names to product lists
        """
        results = {}
        
        for name, scraper in self.scrapers.items():
            try:
                print(f"Searching {scraper.website_name}...")
                products = scraper.search_products(query, max_results_per_site)
                results[name] = products
                print(f"Found {len(products)} products on {scraper.website_name}")
            except Exception as e:
                print(f"Error searching {name}: {e}")
                results[name] = []
        
        return results
    
    def search_website(self, website: str, query: str, max_results: int = 10) -> List[Product]:
        """
        Search for products on a specific website.
        
        Args:
            website: Website name ('alza', 'allegro', or 'smarty')
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of Product objects
        """
        scraper = self.scrapers.get(website.lower())
        if not scraper:
            raise ValueError(f"Unknown website: {website}. Choose from: {list(self.scrapers.keys())}")
        
        return scraper.search_products(query, max_results)
    
    def track_product(self, url: str) -> bool:
        """
        Start tracking a product by its URL.
        Determines the website from URL and fetches product details.
        
        Args:
            url: Product URL
            
        Returns:
            True if successful, False otherwise
        """
        # Determine which scraper to use based on URL
        scraper = None
        for s in self.scrapers.values():
            if s.config['base_url'] in url:
                scraper = s
                break
        
        if not scraper:
            print(f"Could not determine website for URL: {url}")
            return False
        
        try:
            # Get product details
            product = scraper.get_product_details(url)
            if not product:
                print(f"Could not fetch product details from {url}")
                return False
            
            # Add to database
            self.db.add_product(
                name=product.name,
                url=product.url,
                website=product.website,
                image_url=product.image_url
            )
            
            # Add price record
            self.db.add_price_record(
                product_url=product.url,
                price=product.price,
                currency=product.currency,
                availability=product.availability,
                rating=product.rating,
                reviews_count=product.reviews_count
            )
            
            print(f"Successfully added {product.name} to tracking")
            return True
            
        except Exception as e:
            print(f"Error tracking product: {e}")
            return False
    
    def update_tracked_products(self) -> Dict[str, int]:
        """
        Update prices for all tracked products.
        
        Returns:
            Dictionary with update statistics
        """
        products = self.db.get_all_products()
        stats = {
            'total': len(products),
            'updated': 0,
            'failed': 0
        }
        
        for product in products:
            try:
                # Determine scraper
                scraper = None
                for s in self.scrapers.values():
                    if s.config['base_url'] in product.url:
                        scraper = s
                        break
                
                if not scraper:
                    print(f"No scraper found for {product.url}")
                    stats['failed'] += 1
                    continue
                
                # Fetch updated product details
                updated_product = scraper.get_product_details(product.url)
                if not updated_product:
                    print(f"Failed to fetch details for {product.name}")
                    stats['failed'] += 1
                    continue
                
                # Add new price record
                self.db.add_price_record(
                    product_url=updated_product.url,
                    price=updated_product.price,
                    currency=updated_product.currency,
                    availability=updated_product.availability,
                    rating=updated_product.rating,
                    reviews_count=updated_product.reviews_count
                )
                
                stats['updated'] += 1
                print(f"Updated {product.name}: {updated_product.price} {updated_product.currency}")
                
            except Exception as e:
                print(f"Error updating {product.name}: {e}")
                stats['failed'] += 1
        
        return stats
    
    def get_price_history(self, product_url: str, limit: int = None):
        """
        Get price history for a tracked product.
        
        Args:
            product_url: Product URL
            limit: Maximum number of records
            
        Returns:
            List of price history records
        """
        return self.db.get_price_history(product_url, limit)
    
    def get_tracked_products(self):
        """
        Get all tracked products.
        
        Returns:
            List of ProductRecord objects
        """
        return self.db.get_all_products()
    
    def close(self):
        """Close database connection."""
        self.db.close()
