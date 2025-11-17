# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/ThejamesX/Scraper.git
cd Scraper

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Search for Products

Search across all supported websites (Alza, Allegro, Smarty):

```bash
python main.py search "Soundbar"
```

Search on a specific website:

```bash
python main.py search "Soundbar" --website alza
python main.py search "wireless headphones" --website allegro
python main.py search "laptop" --website smarty
```

Limit results:

```bash
python main.py search "smartphone" --max-results 5
```

### 2. Track Product Prices

Start tracking a product by copying its URL from one of the supported websites:

```bash
# Track from Alza
python main.py track "https://www.alza.cz/samsung-hw-q60c-en-d7569191.htm"

# Track from Allegro
python main.py track "https://allegro.pl/oferta/samsung-galaxy-s24-..."

# Track from Smarty
python main.py track "https://www.smarty.cz/produkt/..."
```

### 3. View Tracked Products

List all products you're currently tracking:

```bash
python main.py list
```

Example output:
```
╒══════╤═══════════════════════════════════════════╤════════════╤═══════════════╤══════════════╕
│   ID │ Name                                      │ Website    │ Latest Price  │ Added        │
╞══════╪═══════════════════════════════════════════╪════════════╪═══════════════╪══════════════╡
│    1 │ Samsung HW-Q60C                           │ Alza.cz    │ 6990.0 CZK    │ 2025-11-17   │
│    2 │ Sony WH-1000XM5                           │ Allegro.pl │ 1299.0 PLN    │ 2025-11-17   │
╘══════╧═══════════════════════════════════════════╧════════════╧═══════════════╧══════════════╛
```

### 4. Update Prices

Fetch the latest prices for all tracked products:

```bash
python main.py update
```

This will:
- Visit each tracked product's page
- Scrape the current price
- Store it in the database with a timestamp
- Display a summary of updates

### 5. View Price History

View price changes for a tracked product:

By product ID (from the `list` command):
```bash
python main.py history --id 1
```

By URL:
```bash
python main.py history --url "https://www.alza.cz/samsung-hw-q60c-en-d7569191.htm"
```

Limit history entries:
```bash
python main.py history --id 1 --limit 10
```

Example output:
```
╒══════════════════╤═══════════╤════════════════╕
│ Date             │ Price     │ Availability   │
╞══════════════════╪═══════════╪════════════════╡
│ 2025-11-17 14:30 │ 6990 CZK  │ In Stock       │
│ 2025-11-16 10:15 │ 7490 CZK  │ In Stock       │
│ 2025-11-15 08:45 │ 7490 CZK  │ In Stock       │
╘══════════════════╧═══════════╧════════════════╛
```

## Programmatic Usage

You can also use the scraper in your Python code:

```python
from scraper.scraper_manager import ScraperManager

# Initialize the manager
manager = ScraperManager()

# Search for products across all websites
results = manager.search_all("gaming laptop", max_results_per_site=5)
for website, products in results.items():
    print(f"{website}: {len(products)} products found")
    for product in products:
        print(f"  - {product.name}: {product.price} {product.currency}")

# Track a product
manager.track_product("https://www.alza.cz/product-url")

# Update all tracked products
stats = manager.update_tracked_products()
print(f"Updated: {stats['updated']}, Failed: {stats['failed']}")

# View price history
history = manager.get_price_history(product_url, limit=10)
for record in history:
    print(f"{record.scraped_at}: {record.price} {record.currency}")

# Always close the connection when done
manager.close()
```

## Automation with Cron

To automatically update prices daily, add a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * cd /path/to/Scraper && python main.py update
```

Or on Windows with Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 8:00 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `main.py update`
7. Start in: `C:\path\to\Scraper`

## Database Management

The scraper uses SQLite database (`price_tracker.db` by default).

### Custom Database Location

```bash
python main.py --database /path/to/custom.db search "product"
```

### Backup Database

```bash
cp price_tracker.db price_tracker_backup.db
```

### View Database Directly

```bash
sqlite3 price_tracker.db
sqlite> SELECT * FROM products;
sqlite> SELECT * FROM price_history ORDER BY scraped_at DESC LIMIT 10;
sqlite> .quit
```

## Tips & Best Practices

1. **Start Small**: Begin by tracking a few products to understand the system
2. **Regular Updates**: Run updates daily or weekly to build price history
3. **Check Selectors**: If scraping fails, website layouts may have changed
4. **Respect Rate Limits**: Don't update too frequently (once daily is reasonable)
5. **Backup Data**: Regularly backup your `price_tracker.db` file

## Troubleshooting

**Problem**: No products found when searching

**Solutions**:
- Verify your internet connection
- The website may be temporarily down
- CSS selectors may have changed (check config files)
- Try a different search query

---

**Problem**: Cannot track a product

**Solutions**:
- Ensure the URL is from a supported website (Alza, Allegro, Smarty)
- Check that the product page is accessible in your browser
- Verify the URL format matches the expected pattern

---

**Problem**: Database errors

**Solutions**:
- Ensure you have write permissions in the directory
- Check available disk space
- Try deleting the database and starting fresh

## Next Steps

1. Run your first search: `python main.py search "your product"`
2. Track some products you're interested in
3. Set up automated updates with cron/Task Scheduler
4. Monitor price changes over time

For more details, see the main [README.md](README.md)
