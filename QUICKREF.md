# Quick Reference

## Common Commands

### Search
```bash
# Search all websites
python main.py search "product name"

# Search specific website
python main.py search "product name" --website alza
python main.py search "product name" --website allegro
python main.py search "product name" --website smarty

# Limit results
python main.py search "product name" --max-results 5
```

### Track
```bash
# Track a product
python main.py track "https://www.alza.cz/product-url"
python main.py track "https://allegro.pl/oferta/product-url"
python main.py track "https://www.smarty.cz/product-url"
```

### Manage
```bash
# List all tracked products
python main.py list

# Update all tracked products
python main.py update

# View price history by ID
python main.py history --id 1

# View price history by URL
python main.py history --url "https://www.alza.cz/product-url"

# Limit history entries
python main.py history --id 1 --limit 10
```

### Custom Database
```bash
python main.py --database /path/to/db.db search "product"
```

## Python API

```python
from scraper.scraper_manager import ScraperManager

manager = ScraperManager()

# Search
results = manager.search_all("product", max_results_per_site=10)
products = manager.search_website("alza", "product", max_results=10)

# Track
manager.track_product("https://www.alza.cz/product-url")

# Update
stats = manager.update_tracked_products()

# History
history = manager.get_price_history(product_url, limit=10)

# List
products = manager.get_tracked_products()

# Close
manager.close()
```

## Supported Websites

| Website | Country | URL |
|---------|---------|-----|
| Alza.cz | Czech Republic | https://www.alza.cz |
| Allegro.pl | Poland | https://allegro.pl |
| Smarty.cz | Czech Republic | https://www.smarty.cz |

## File Structure

```
scraper/
├── base_scraper.py       - Abstract base class
├── scraper_manager.py    - Unified manager
├── scrapers/             - Website scrapers
│   ├── alza_scraper.py
│   ├── allegro_scraper.py
│   └── smarty_scraper.py
├── models/               - Database models
│   └── database.py
└── config/               - Configuration
    └── __init__.py
```

## Adding New Website

1. Add config to `scraper/config/__init__.py`
2. Create scraper in `scraper/scrapers/new_site.py`
3. Import in `scraper/scrapers/__init__.py`
4. Register in `ScraperManager.__init__()`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No products found | Check internet, verify selectors |
| Cannot track product | Verify URL from supported site |
| Database errors | Check permissions, disk space |
| Import errors | Run `pip install -r requirements.txt` |

## Dependencies

Install: `pip install -r requirements.txt`

Core:
- beautifulsoup4
- requests
- lxml
- sqlalchemy
- tabulate

Optional:
- selenium (for JavaScript sites)

## Testing

```bash
# Run all tests
python -m pytest tests/test_scrapers.py -v

# Run specific test
python -m pytest tests/test_scrapers.py::TestBaseScraper::test_clean_price -v
```

## Examples

See `example.py` for working examples of all features.

## Documentation

- **README.md** - Full documentation
- **USAGE.md** - User guide
- **IMPLEMENTATION.md** - Technical details
- **QUICKREF.md** - This file
