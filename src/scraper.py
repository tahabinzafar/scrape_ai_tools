
import concurrent.futures
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import aiohttp
import asyncio
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-javascript")  # Disable JS for faster loading
    chrome_options.page_load_strategy = 'eager'  # Don't wait for all resources
    return webdriver.Chrome(options=chrome_options)

def get_page_source(url, timeout=30):
    driver = setup_driver()
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        
        # Wait for first tool to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tool-item-columns-new"))
        )
        
        # Single scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)  # Brief wait for any dynamic content
        
        return driver.page_source
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return None
    finally:
        driver.quit()

def parse_tools(page_source, model):
    if not page_source:
        return []
        
    soup = BeautifulSoup(page_source, 'html.parser')
    tools = []
    
    for item in soup.find_all("div", class_="tool-item-columns-new"):
        try:
            tool = {
                "name": item.find("a", class_="tool-item-link---new").text.strip(),
                "description": item.find("div", class_="tool-item-description-box---new").text.strip(),
                "category": item.find("div", class_="text-block-53").text.strip() if item.find("div", class_="text-block-53") else "N/A",
                "link": item.find("a", class_="tool-item-new-window---new").get('href', 'N/A'),
                "upvotes": item.find("div", class_="jetboost-item-total-favorites-vd2l").text.strip() if item.find("div", class_="jetboost-item-total-favorites-vd2l") else "0",
                "pricing_model": model
            }
            tools.append(tool)
        except AttributeError:
            continue
            
    return tools

def process_url(args):
    model, url = args
    page_source = get_page_source(url)
    return parse_tools(page_source, model)

def main():
    pricing_models = {
        "Free": "https://www.futuretools.io/?pricing-model=free",
        "Freemium": "https://www.futuretools.io/?pricing-model=freemium",
        "Github": "https://www.futuretools.io/?pricing-model=github",
        "Google Colab": "https://www.futuretools.io/?pricing-model=google-colab",
        "Open Source": "https://www.futuretools.io/?pricing-model=open-source",
        "Paid": "https://www.futuretools.io/?pricing-model=paid"
    }
    
    all_tools = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = list(executor.map(process_url, pricing_models.items()))
        for tools in futures:
            all_tools.extend(tools)
    
    df = pd.DataFrame(all_tools)
    df.to_excel('futuretools_data.xlsx', index=False)
    print(f"Total tools saved: {len(all_tools)}")

if __name__ == "__main__":
    main()
    
 
