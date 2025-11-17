#!/usr/bin/env python3
"""
Command-line interface for the price tracker scraper.
"""

import argparse
import sys
from tabulate import tabulate
from scraper.scraper_manager import ScraperManager


def search_command(args):
    """Handle search command."""
    manager = ScraperManager(args.database)
    
    if args.website:
        # Search specific website
        products = manager.search_website(args.website, args.query, args.max_results)
        print(f"\n=== Results from {args.website.upper()} ===")
        display_products(products)
    else:
        # Search all websites
        results = manager.search_all(args.query, args.max_results)
        for website, products in results.items():
            print(f"\n=== Results from {website.upper()} ===")
            display_products(products)
    
    manager.close()


def track_command(args):
    """Handle track command."""
    manager = ScraperManager(args.database)
    
    success = manager.track_product(args.url)
    if success:
        print(f"✓ Successfully tracking product")
    else:
        print(f"✗ Failed to track product")
    
    manager.close()


def update_command(args):
    """Handle update command."""
    manager = ScraperManager(args.database)
    
    print("Updating tracked products...")
    stats = manager.update_tracked_products()
    
    print(f"\n=== Update Summary ===")
    print(f"Total products: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Failed: {stats['failed']}")
    
    manager.close()


def list_command(args):
    """Handle list command."""
    manager = ScraperManager(args.database)
    
    products = manager.get_tracked_products()
    
    if not products:
        print("No tracked products found.")
        manager.close()
        return
    
    print(f"\n=== Tracked Products ({len(products)}) ===\n")
    
    data = []
    for product in products:
        latest_price = manager.db.get_latest_price(product.url)
        price_str = f"{latest_price.price} {latest_price.currency}" if latest_price else "N/A"
        data.append([
            product.id,
            product.name[:50],
            product.website,
            price_str,
            product.created_at.strftime('%Y-%m-%d')
        ])
    
    print(tabulate(data, headers=['ID', 'Name', 'Website', 'Latest Price', 'Added'], tablefmt='grid'))
    
    manager.close()


def history_command(args):
    """Handle history command."""
    manager = ScraperManager(args.database)
    
    # Get product by URL or ID
    if args.url:
        product_url = args.url
    elif args.id:
        products = manager.get_tracked_products()
        product = next((p for p in products if p.id == args.id), None)
        if not product:
            print(f"Product with ID {args.id} not found.")
            manager.close()
            return
        product_url = product.url
    else:
        print("Please provide either --url or --id")
        manager.close()
        return
    
    history = manager.get_price_history(product_url, args.limit)
    
    if not history:
        print("No price history found.")
        manager.close()
        return
    
    print(f"\n=== Price History ===\n")
    
    data = []
    for record in history:
        data.append([
            record.scraped_at.strftime('%Y-%m-%d %H:%M'),
            f"{record.price} {record.currency}",
            record.availability or "N/A"
        ])
    
    print(tabulate(data, headers=['Date', 'Price', 'Availability'], tablefmt='grid'))
    
    manager.close()


def display_products(products):
    """Display product list in a table."""
    if not products:
        print("No products found.")
        return
    
    data = []
    for product in products:
        data.append([
            product.name[:60],
            f"{product.price} {product.currency}",
            product.availability or "N/A",
            product.url[:50] + "..."
        ])
    
    print(tabulate(data, headers=['Name', 'Price', 'Availability', 'URL'], tablefmt='grid'))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Web scraper for tracking product prices across e-commerce sites'
    )
    parser.add_argument('--database', '-d', default='price_tracker.db',
                       help='Database file path (default: price_tracker.db)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for products')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--website', '-w', choices=['alza', 'allegro', 'smarty'],
                              help='Search specific website only')
    search_parser.add_argument('--max-results', '-n', type=int, default=10,
                              help='Maximum results per website (default: 10)')
    search_parser.set_defaults(func=search_command)
    
    # Track command
    track_parser = subparsers.add_parser('track', help='Track a product by URL')
    track_parser.add_argument('url', help='Product URL')
    track_parser.set_defaults(func=track_command)
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update all tracked products')
    update_parser.set_defaults(func=update_command)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked products')
    list_parser.set_defaults(func=list_command)
    
    # History command
    history_parser = subparsers.add_parser('history', help='View price history')
    history_parser.add_argument('--url', help='Product URL')
    history_parser.add_argument('--id', type=int, help='Product ID from list')
    history_parser.add_argument('--limit', '-n', type=int, default=20,
                               help='Maximum number of records (default: 20)')
    history_parser.set_defaults(func=history_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
