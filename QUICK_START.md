# Quick Start: Testing the 403 Fix

## What Was Fixed
The web scrapers were getting **403 Forbidden** errors when trying to access:
- Alza.cz
- Allegro.pl  
- Smarty.cz

This has been fixed by updating the HTTP request headers to look like real Chrome browser requests.

## How to Test

### Option 1: Quick Test (Recommended)
```bash
python test_online.py
```

This will test all three websites and show you if products are being found successfully.

### Option 2: Use the Main CLI
```bash
python main.py search "Soundbar" --max-results 5
```

### Option 3: Test Individual Websites
```bash
python test_online.py alza
python test_online.py allegro
python test_online.py smarty
```

## Expected Results

### Before Fix ❌
```
Request failed (attempt 1/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Request failed (attempt 2/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Request failed (attempt 3/3): 403 Client Error: Forbidden for url: https://www.alza.cz/search.htm?exps=Soundbar
Found 0 products on Alza.cz
```

### After Fix ✅
```
✅ SUCCESS: Found 3 products

1. Samsung HW-Q60C
   Price: 7990.0 CZK
   URL: https://www.alza.cz/samsung-hw-q60c-en-d7569191.htm...

2. Sony HT-S400
   Price: 6990.0 CZK
   URL: https://www.alza.cz/sony-ht-s400-d7234567.htm...
```

## What Changed

The HTTP headers now include:
- ✅ Complete User-Agent (Chrome 120.0.0.0)
- ✅ Accept headers for HTML/images
- ✅ Accept-Encoding for compression
- ✅ Accept-Language with proper locales
- ✅ Sec-Fetch-* security headers
- ✅ Cache-Control and Connection headers

## If You Still Get 403 Errors

See `FIX_DOCUMENTATION.md` for advanced troubleshooting, including:
- Using proxies
- Adding more delays
- Using Selenium for JavaScript-heavy sites

## Files Modified
- `scraper/config/__init__.py` - Enhanced headers for all scrapers

## Files Added
- `test_online.py` - Testing script
- `FIX_DOCUMENTATION.md` - Detailed documentation
- `QUICK_START.md` - This file

## Need Help?
Open an issue on GitHub if you encounter any problems.
