#!/usr/bin/env python3
"""
Example usage of the price tracker scraper.
This script demonstrates the main features of the scraper.
"""

from scraper.scraper_manager import ScraperManager
from scraper.base_scraper import Product


def main():
    print("=== E-Commerce Price Tracker - Example Usage ===\n")
    
    # Initialize the scraper manager
    manager = ScraperManager(db_path='example_tracker.db')
    
    # Example 1: Search for products across all websites
    print("Example 1: Searching for 'Soundbar' across all websites...")
    results = manager.search_all("Soundbar", max_results_per_site=3)
    
    for website, products in results.items():
        print(f"\n{website.upper()}: Found {len(products)} products")
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product.name[:60]}")
            print(f"     Price: {product.price} {product.currency}")
            print(f"     URL: {product.url[:70]}...")
    
    # Example 2: Search on a specific website
    print("\n" + "="*80)
    print("Example 2: Searching 'headphones' on Alza only...")
    alza_products = manager.search_website("alza", "headphones", max_results=3)
    
    for i, product in enumerate(alza_products, 1):
        print(f"{i}. {product.name}")
        print(f"   Price: {product.price} {product.currency}")
        print(f"   Availability: {product.availability or 'N/A'}")
    
    # Example 3: Track a product (commented out to avoid actual tracking)
    # print("\n" + "="*80)
    # print("Example 3: Tracking a product...")
    # if alza_products:
    #     product_url = alza_products[0].url
    #     manager.track_product(product_url)
    #     print(f"Now tracking: {alza_products[0].name}")
    
    # Example 4: List tracked products
    print("\n" + "="*80)
    print("Example 4: Listing tracked products...")
    tracked = manager.get_tracked_products()
    print(f"Currently tracking {len(tracked)} products")
    
    for product in tracked[:5]:  # Show first 5
        latest_price = manager.db.get_latest_price(product.url)
        if latest_price:
            print(f"- {product.name[:50]}")
            print(f"  Latest price: {latest_price.price} {latest_price.currency}")
    
    # Example 5: Price history
    if tracked:
        print("\n" + "="*80)
        print("Example 5: Price history for first tracked product...")
        product = tracked[0]
        history = manager.get_price_history(product.url, limit=5)
        
        print(f"Product: {product.name}")
        print(f"Price history ({len(history)} records):")
        for record in history:
            print(f"  {record.scraped_at.strftime('%Y-%m-%d %H:%M')}: "
                  f"{record.price} {record.currency}")
    
    # Clean up
    manager.close()
    print("\n" + "="*80)
    print("Example completed!")


if __name__ == '__main__':
    main()
