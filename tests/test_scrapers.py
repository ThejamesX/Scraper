"""Tests for the scraper functionality."""

import pytest
from scraper.base_scraper import BaseScraper, Product
from scraper.scrapers import AlzaScraper, AllegroScraper, SmartyScraper
from scraper.models import Database
from scraper.scraper_manager import ScraperManager
import os
from datetime import datetime


class TestBaseScraper:
    """Test the base scraper functionality."""
    
    def test_clean_price(self):
        """Test price cleaning function."""
        scraper = AlzaScraper()
        
        # Test various price formats
        assert scraper.clean_price("$123.45") == 123.45
        assert scraper.clean_price("123,45 €") == 123.45
        assert scraper.clean_price("1 234,56 Kč") == 1234.56
        assert scraper.clean_price("1,234.56") == 1234.56
        assert scraper.clean_price("invalid") is None
        assert scraper.clean_price("") is None
    
    def test_extract_currency(self):
        """Test currency extraction."""
        scraper = AlzaScraper()
        
        assert scraper.extract_currency("$123.45") == "USD"
        assert scraper.extract_currency("123,45 €") == "EUR"
        assert scraper.extract_currency("123,45 Kč") == "CZK"
        assert scraper.extract_currency("123,45 zł") == "PLN"
        assert scraper.extract_currency("123.45") == "USD"  # Default


class TestProduct:
    """Test Product dataclass."""
    
    def test_product_creation(self):
        """Test creating a product."""
        product = Product(
            name="Test Product",
            price=99.99,
            currency="USD",
            url="https://example.com/product",
            website="Example"
        )
        
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.currency == "USD"
        assert product.url == "https://example.com/product"
        assert product.website == "Example"
        assert isinstance(product.scraped_at, datetime)
    
    def test_product_optional_fields(self):
        """Test product with optional fields."""
        product = Product(
            name="Test Product",
            price=99.99,
            currency="USD",
            url="https://example.com/product",
            website="Example",
            image_url="https://example.com/image.jpg",
            availability="In Stock",
            rating=4.5,
            reviews_count=100
        )
        
        assert product.image_url == "https://example.com/image.jpg"
        assert product.availability == "In Stock"
        assert product.rating == 4.5
        assert product.reviews_count == 100


class TestDatabase:
    """Test database functionality."""
    
    @pytest.fixture
    def db(self):
        """Create a test database."""
        db_path = 'test_db.db'
        db = Database(db_path)
        yield db
        db.close()
        # Clean up
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_add_product(self, db):
        """Test adding a product."""
        product = db.add_product(
            name="Test Product",
            url="https://example.com/test",
            website="Example",
            image_url="https://example.com/image.jpg"
        )
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.url == "https://example.com/test"
    
    def test_add_price_record(self, db):
        """Test adding a price record."""
        # First add a product
        db.add_product(
            name="Test Product",
            url="https://example.com/test",
            website="Example"
        )
        
        # Then add a price record
        price_record = db.add_price_record(
            product_url="https://example.com/test",
            price=99.99,
            currency="USD",
            availability="In Stock"
        )
        
        assert price_record.id is not None
        assert price_record.price == 99.99
        assert price_record.currency == "USD"
    
    def test_get_price_history(self, db):
        """Test retrieving price history."""
        url = "https://example.com/test"
        
        # Add product
        db.add_product(name="Test", url=url, website="Example")
        
        # Add multiple price records
        db.add_price_record(url, 100.0, "USD")
        db.add_price_record(url, 95.0, "USD")
        db.add_price_record(url, 90.0, "USD")
        
        # Get history
        history = db.get_price_history(url)
        assert len(history) == 3
        assert history[0].price == 90.0  # Most recent first
    
    def test_get_latest_price(self, db):
        """Test getting latest price."""
        url = "https://example.com/test"
        
        db.add_product(name="Test", url=url, website="Example")
        db.add_price_record(url, 100.0, "USD")
        db.add_price_record(url, 95.0, "USD")
        
        latest = db.get_latest_price(url)
        assert latest.price == 95.0


class TestScrapers:
    """Test scraper implementations."""
    
    def test_alza_scraper_initialization(self):
        """Test Alza scraper initialization."""
        scraper = AlzaScraper()
        assert scraper.website_name == "Alza.cz"
        assert scraper.config is not None
    
    def test_allegro_scraper_initialization(self):
        """Test Allegro scraper initialization."""
        scraper = AllegroScraper()
        assert scraper.website_name == "Allegro.pl"
        assert scraper.config is not None
    
    def test_smarty_scraper_initialization(self):
        """Test Smarty scraper initialization."""
        scraper = SmartyScraper()
        assert scraper.website_name == "Smarty.cz"
        assert scraper.config is not None


class TestScraperManager:
    """Test scraper manager."""
    
    @pytest.fixture
    def manager(self):
        """Create a test scraper manager."""
        db_path = 'test_manager.db'
        manager = ScraperManager(db_path)
        yield manager
        manager.close()
        if os.path.exists(db_path):
            os.remove(db_path)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert len(manager.scrapers) == 3
        assert 'alza' in manager.scrapers
        assert 'allegro' in manager.scrapers
        assert 'smarty' in manager.scrapers
    
    def test_search_website_invalid(self, manager):
        """Test searching invalid website."""
        with pytest.raises(ValueError):
            manager.search_website("invalid", "test")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
