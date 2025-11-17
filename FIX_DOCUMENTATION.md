# Fix for 403 Forbidden Errors

## Problem
The web scrapers were encountering 403 Forbidden errors when trying to access:
- Alza.cz
- Allegro.pl
- Smarty.cz

### Error Messages
```
Request failed (attempt 1/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Request failed (attempt 2/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Request failed (attempt 3/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Found 0 products on Alza.cz
```

## Root Cause
The HTTP headers being sent with the requests were too basic and were being detected as automated/bot traffic by the websites' anti-bot protection systems. The original headers only included:
- A truncated User-Agent string
- Basic Accept-Language header

Modern websites expect a full set of HTTP headers that match legitimate browser requests.

## Solution
Enhanced the HTTP headers in `/scraper/config/__init__.py` for all three scrapers to include comprehensive browser headers that mimic Chrome 120.0.0.0:

### Updated Headers
```python
'headers': {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'cs-CZ,cs;q=0.9,en-US;q=0.8,en;q=0.7',  # or pl-PL for Allegro
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}
```

### Key Improvements
1. **Complete User-Agent**: Full Chrome browser identification string
2. **Accept Header**: Comprehensive list of accepted content types with quality values
3. **Accept-Encoding**: Supports modern compression (gzip, deflate, brotli)
4. **Accept-Language**: Proper locale with quality values
5. **Sec-Fetch-* Headers**: Modern browser security headers that indicate legitimate user navigation
6. **Cache-Control**: Proper caching behavior
7. **Connection**: Keep-alive for better performance and more realistic behavior

## Testing Online

To test the fix when you have internet access:

```bash
# Test all scrapers
python test_online.py

# Test a specific scraper
python test_online.py alza
python test_online.py allegro
python test_online.py smarty
```

Or use the main CLI:
```bash
python main.py search "Soundbar" --max-results 5
```

## Expected Results
- Requests should no longer return 403 Forbidden errors
- Products should be successfully scraped from all three websites
- Search results should display product names, prices, and URLs

## Additional Notes

### If 403 Errors Persist
Some websites may have additional protection mechanisms:

1. **Rate Limiting**: Add delays between requests
   - Already implemented with `RETRY_DELAY` in config
   
2. **IP-based Blocking**: May need to use:
   - Proxy rotation
   - VPN services
   
3. **More Advanced Bot Detection**: May require:
   - Selenium with real browser automation
   - Session/cookie management
   - JavaScript execution

### Respectful Scraping
Always ensure you:
- Respect robots.txt
- Add delays between requests
- Don't overload servers
- Comply with Terms of Service
- Consider using official APIs when available

## Files Modified
- `/scraper/config/__init__.py` - Enhanced HTTP headers for all three scrapers

## Files Added
- `/test_online.py` - Manual testing script for online verification
- `/FIX_DOCUMENTATION.md` - This documentation file
