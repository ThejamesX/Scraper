"""Database models for price tracking."""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class ProductRecord(Base):
    """Product database model for storing product information."""
    
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    website = Column(String(100), nullable=False)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Product(name='{self.name}', website='{self.website}')>"


class PriceHistory(Base):
    """Price history model for tracking price changes over time."""
    
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_url = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    availability = Column(String(200))
    rating = Column(Float)
    reviews_count = Column(Integer)
    scraped_at = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<PriceHistory(url='{self.product_url[:50]}...', price={self.price}, date='{self.scraped_at}')>"


class Database:
    """Database manager for product and price history."""
    
    def __init__(self, db_path: str = 'price_tracker.db'):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_product(self, name: str, url: str, website: str, image_url: str = None) -> ProductRecord:
        """
        Add or update a product in the database.
        
        Args:
            name: Product name
            url: Product URL
            website: Website name
            image_url: Product image URL
            
        Returns:
            ProductRecord object
        """
        # Check if product already exists
        product = self.session.query(ProductRecord).filter_by(url=url).first()
        
        if product:
            # Update existing product
            product.name = name
            product.website = website
            product.image_url = image_url
            product.updated_at = datetime.now()
        else:
            # Create new product
            product = ProductRecord(
                name=name,
                url=url,
                website=website,
                image_url=image_url
            )
            self.session.add(product)
        
        self.session.commit()
        return product
    
    def add_price_record(self, product_url: str, price: float, currency: str,
                        availability: str = None, rating: float = None,
                        reviews_count: int = None) -> PriceHistory:
        """
        Add a price record to the history.
        
        Args:
            product_url: Product URL
            price: Product price
            currency: Currency code
            availability: Availability status
            rating: Product rating
            reviews_count: Number of reviews
            
        Returns:
            PriceHistory object
        """
        price_record = PriceHistory(
            product_url=product_url,
            price=price,
            currency=currency,
            availability=availability,
            rating=rating,
            reviews_count=reviews_count
        )
        
        self.session.add(price_record)
        self.session.commit()
        return price_record
    
    def get_price_history(self, product_url: str, limit: int = None):
        """
        Get price history for a product.
        
        Args:
            product_url: Product URL
            limit: Maximum number of records to return
            
        Returns:
            List of PriceHistory objects
        """
        query = self.session.query(PriceHistory).filter_by(product_url=product_url).order_by(PriceHistory.scraped_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def get_all_products(self):
        """
        Get all tracked products.
        
        Returns:
            List of ProductRecord objects
        """
        return self.session.query(ProductRecord).all()
    
    def get_latest_price(self, product_url: str):
        """
        Get the latest price for a product.
        
        Args:
            product_url: Product URL
            
        Returns:
            PriceHistory object or None
        """
        return self.session.query(PriceHistory).filter_by(product_url=product_url).order_by(PriceHistory.scraped_at.desc()).first()
    
    def close(self):
        """Close database connection."""
        self.session.close()
