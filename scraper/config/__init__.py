"""Configuration for different e-commerce websites."""

# Alza configuration (Czech/Slovak e-commerce)
ALZA_CONFIG = {
    'base_url': 'https://www.alza.cz',
    'search_url': 'https://www.alza.cz/search.htm',
    'selectors': {
        'search_results': 'div.browsingitem',
        'product_name': 'a.name',
        'product_price': 'span.price-box__price',
        'product_link': 'a.name',
        'product_image': 'img.js-productImageItem',
        'availability': 'span.avlVal',
        'rating': 'div.rating',
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'cs,en;q=0.9',
    }
}

# Allegro configuration (Polish e-commerce)
ALLEGRO_CONFIG = {
    'base_url': 'https://allegro.pl',
    'search_url': 'https://allegro.pl/listing',
    'selectors': {
        'search_results': 'article[data-role="offer"]',
        'product_name': 'h2',
        'product_price': 'span[class*="price"]',
        'product_link': 'a[href*="/oferta/"]',
        'product_image': 'img[alt]',
        'availability': 'span[data-role="delivery"]',
        'rating': 'div[data-role="rating"]',
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'pl,en;q=0.9',
    }
}

# Smarty configuration (Czech/Slovak e-commerce)
SMARTY_CONFIG = {
    'base_url': 'https://www.smarty.cz',
    'search_url': 'https://www.smarty.cz/search',
    'selectors': {
        'search_results': 'div.product-item',
        'product_name': 'h3.product-name',
        'product_price': 'span.price',
        'product_link': 'a.product-link',
        'product_image': 'img.product-image',
        'availability': 'span.availability',
        'rating': 'div.rating-stars',
    },
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'cs,en;q=0.9',
    }
}

# Request settings
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
