# FutureTools Scraper  

This script scrapes tool data from [FutureTools.io](https://www.futuretools.io) based on different pricing models. It extracts tool names, descriptions, categories, links, upvotes, and pricing information, then saves the data to an Excel file.  

## Why Selenium?  
FutureTools.io loads content dynamically, meaning standard HTTP requests (`requests` or `BeautifulSoup`) can't retrieve all the data. Selenium is used to:  
- Load JavaScript-rendered content.  
- Scroll down to ensure all tools are visible.  
- Wait for elements to appear before scraping.  

## How It Works  
1. Uses Selenium to load the webpage and scroll to reveal all tools.  
2. Parses tool details using BeautifulSoup.  
3. Runs multiple scrapes in parallel with `ThreadPoolExecutor`.  
4. Saves the extracted data to an Excel file.  

## Requirements  
- Python  
- Selenium  
- BeautifulSoup  
- Pandas  
