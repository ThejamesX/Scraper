# E-Commerce Price Tracker

A scalable web scraper for tracking product prices across multiple e-commerce platforms (Alza, Allegro, and Smarty). This tool allows you to search for products, track their prices over time, and analyze price history.

## Features

- 🔍 **Multi-site Search**: Search for products across Alza.cz, Allegro.pl, and Smarty.cz simultaneously
- 📊 **Price History Tracking**: Monitor price changes over time with SQLite database storage
- 🏗️ **Scalable Architecture**: Easy to add new e-commerce websites with abstract base classes
- 🔄 **Automatic Updates**: Batch update all tracked products with a single command
- 💾 **Database Persistence**: SQLite database for storing product information and price history
- 🛠️ **CLI Interface**: Command-line interface for easy interaction

## Architecture

The project uses a modular, scalable architecture:

```
scraper/
├── base_scraper.py      # Abstract base class for all scrapers
├── scrapers/            # Website-specific scraper implementations
│   ├── alza_scraper.py
│   ├── allegro_scraper.py
│   └── smarty_scraper.py
├── models/              # Database models
│   └── database.py
├── config/              # Configuration for each website
│   └── __init__.py
└── scraper_manager.py   # Unified manager for all scrapers
```

### Design Principles

1. **Separation of Concerns**: Each website has its own scraper module with search and scraping logic
2. **Extensibility**: Adding new websites requires implementing the `BaseScraper` interface
3. **Configuration-based**: Website-specific selectors and URLs are in configuration files
4. **Database Abstraction**: SQLAlchemy ORM for database operations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ThejamesX/Scraper.git
cd Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The scraper provides a command-line interface with several commands:

### Search for Products

Search across all websites:
```bash
python main.py search "Soundbar"
```

Search on a specific website:
```bash
python main.py search "Soundbar" --website alza
python main.py search "Soundbar" --website allegro
python main.py search "Soundbar" --website smarty
```

Limit search results:
```bash
python main.py search "Soundbar" --max-results 5
```

### Track a Product

Start tracking a product by its URL:
```bash
python main.py track "https://www.alza.cz/samsung-hw-q60c-en-d7569191.htm"
```

### List Tracked Products

View all products you're tracking:
```bash
python main.py list
```

### Update Tracked Products

Update prices for all tracked products:
```bash
python main.py update
```

### View Price History

View price history by product ID:
```bash
python main.py history --id 1
```

View price history by URL:
```bash
python main.py history --url "https://www.alza.cz/product-url"
```

Limit history records:
```bash
python main.py history --id 1 --limit 10
```

### Database Location

By default, the database is stored in `price_tracker.db`. You can specify a custom location:
```bash
python main.py --database /path/to/custom.db search "Soundbar"
```

## Programmatic Usage

You can also use the scraper programmatically in your Python code:

```python
from scraper.scraper_manager import ScraperManager

# Initialize manager
manager = ScraperManager()

# Search for products
results = manager.search_all("Soundbar", max_results_per_site=5)

# Search specific website
products = manager.search_website("alza", "Soundbar", max_results=10)

# Track a product
manager.track_product("https://www.alza.cz/product-url")

# Update all tracked products
stats = manager.update_tracked_products()

# Get price history
history = manager.get_price_history(product_url)

# Close database connection
manager.close()
```

## Adding New Websites

To add support for a new e-commerce website:

1. **Create a configuration** in `scraper/config/__init__.py`:
```python
NEW_SITE_CONFIG = {
    'base_url': 'https://www.example.com',
    'search_url': 'https://www.example.com/search',
    'selectors': {
        'search_results': 'div.product',
        'product_name': 'h2.title',
        'product_price': 'span.price',
        # ... other selectors
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0...',
    }
}
```

2. **Create a scraper class** in `scraper/scrapers/new_site_scraper.py`:
```python
from scraper.base_scraper import BaseScraper, Product
from scraper.config import NEW_SITE_CONFIG

class NewSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.config = NEW_SITE_CONFIG
    
    def get_website_name(self) -> str:
        return "NewSite.com"
    
    def search_products(self, query: str, max_results: int = 10) -> List[Product]:
        # Implement search logic
        pass
    
    def get_product_details(self, url: str) -> Optional[Product]:
        # Implement product detail fetching
        pass
```

3. **Register the scraper** in `scraper/scraper_manager.py`:
```python
from scraper.scrapers.new_site_scraper import NewSiteScraper

self.scrapers = {
    'alza': AlzaScraper(),
    'allegro': AllegroScraper(),
    'smarty': SmartyScraper(),
    'newsite': NewSiteScraper(),  # Add here
}
```

## Dependencies

- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests
- **lxml**: Fast XML/HTML parser
- **selenium**: JavaScript rendering (for dynamic content)
- **sqlalchemy**: Database ORM
- **tabulate**: CLI table formatting
- **pytest**: Testing framework

## Project Structure

```
Scraper/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                   # CLI entry point
├── scraper/                  # Main package
│   ├── __init__.py
│   ├── base_scraper.py       # Abstract base class
│   ├── scraper_manager.py    # Unified manager
│   ├── scrapers/             # Website-specific scrapers
│   │   ├── __init__.py
│   │   ├── alza_scraper.py
│   │   ├── allegro_scraper.py
│   │   └── smarty_scraper.py
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   └── database.py
│   └── config/               # Configuration
│       └── __init__.py
└── tests/                    # Test files
    └── test_scrapers.py
```

## Supported Websites

| Website | Country | Currency | Status |
|---------|---------|----------|--------|
| Alza.cz | Czech Republic/Slovakia | CZK/EUR | ✅ Implemented |
| Allegro.pl | Poland | PLN | ✅ Implemented |
| Smarty.cz | Czech Republic | CZK | ✅ Implemented |

## Notes

- **Respectful Scraping**: The scraper includes delays and retry logic to avoid overloading servers
- **Selector Updates**: Website layouts change; you may need to update CSS selectors in configuration
- **JavaScript Sites**: For heavily JavaScript-based sites, the Selenium integration can be enabled
- **Rate Limiting**: Consider implementing rate limiting for production use
- **Legal Compliance**: Ensure you comply with websites' Terms of Service and robots.txt

## Limitations

- CSS selectors may need updates as websites change their layouts
- Some websites may block automated requests; user-agent rotation may be needed
- JavaScript-heavy sites may require Selenium (currently optional)
- No built-in scheduling (use cron or Task Scheduler for periodic updates)

## Future Enhancements

- [ ] Web UI for easier interaction
- [ ] Price drop notifications via email
- [ ] Export data to CSV/JSON
- [ ] API endpoint for integration with other services
- [ ] Proxy support for avoiding rate limits
- [ ] Multi-threading for faster updates
- [ ] Charts for price history visualization

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please respect the Terms of Service of the websites you scrape.

## Troubleshooting

**Issue**: Products not found
- Check if website selectors are still valid (websites update their layouts)
- Verify the website is accessible
- Check your internet connection

**Issue**: Database errors
- Ensure the database file is writable
- Check disk space
- Try deleting the database file and starting fresh

**Issue**: Slow scraping
- Websites may be rate-limiting your requests
- Consider increasing retry delays
- Use only the websites you need

## Contact

For issues and questions, please open an issue on GitHub.
