#!/usr/bin/env python3
"""
Script to test the scrapers online with real websites.
This should be run when you have internet access to verify the 403 errors are fixed.

Usage:
    python test_online.py
"""

import sys
from scraper.scraper_manager import ScraperManager


def test_all_scrapers():
    """Test all scrapers with a sample query."""
    print("=" * 60)
    print("Testing Web Scrapers Online")
    print("=" * 60)
    print()
    
    query = "Soundbar"
    max_results = 3
    
    manager = ScraperManager()
    
    # Test each scraper individually
    scrapers_to_test = ['alza', 'allegro', 'smarty']
    
    for scraper_name in scrapers_to_test:
        print(f"\n{'=' * 60}")
        print(f"Testing {scraper_name.upper()}")
        print('=' * 60)
        
        try:
            products = manager.search_website(scraper_name, query, max_results)
            
            if products:
                print(f"✅ SUCCESS: Found {len(products)} products")
                print()
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product.name[:60]}")
                    print(f"   Price: {product.price} {product.currency}")
                    print(f"   URL: {product.url[:70]}...")
                    print()
            else:
                print(f"⚠️  WARNING: No products found (might be selector issue)")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    manager.close()
    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)


def test_single_scraper(scraper_name):
    """Test a single scraper."""
    query = "Soundbar"
    max_results = 5
    
    print(f"Testing {scraper_name} with query: '{query}'")
    print("=" * 60)
    
    manager = ScraperManager()
    
    try:
        products = manager.search_website(scraper_name, query, max_results)
        
        if products:
            print(f"✅ Found {len(products)} products:\n")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product.name}")
                print(f"   Price: {product.price} {product.currency}")
                print(f"   Availability: {product.availability or 'N/A'}")
                print(f"   URL: {product.url}")
                print()
        else:
            print("No products found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    manager.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        scraper_name = sys.argv[1].lower()
        if scraper_name in ['alza', 'allegro', 'smarty']:
            test_single_scraper(scraper_name)
        else:
            print(f"Unknown scraper: {scraper_name}")
            print("Available scrapers: alza, allegro, smarty")
    else:
        test_all_scrapers()
