import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_dummy_dataset(output_file):
    """
    Scrapes 'quotes.toscrape.com' using Selenium and BeautifulSoup.
    No APIs, just pure web automation targeting a legal scraping sandbox.
    """
    # 1. EXACT list of free, public URLs to scrape!
    url_list = [
        "http://quotes.toscrape.com/page/1/",
        "http://quotes.toscrape.com/page/2/",
        "http://quotes.toscrape.com/page/3/",
        "http://quotes.toscrape.com/page/4/",
        "http://quotes.toscrape.com/page/5/"
    ]

    # 2. Setup Selenium Chrome WebDriver
    print("Initializing WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Runs invisible in the background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Auto-downloads the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_scraped_data = []

    try:
        # 3. Loop through the list of URLs
        for url in url_list:
            print(f"Scraping URL: {url} ...")
            driver.get(url)
            
            # Brief pause to let the page fully render
            time.sleep(2) 
            
            # 4. Grab the HTML source and pass to BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # 5. Find the exact HTML elements for this specific sandbox site
            # The structure is: <div class="quote"> -> <span class="text"> and <small class="author">
            quote_blocks = soup.find_all('div', class_='quote') 
            
            if not quote_blocks:
                print(f"  -> No data found on {url}.")
                continue

            print(f"  -> Found {len(quote_blocks)} items.")
            
            for block in quote_blocks:
                # Extract text and author
                text = block.find('span', class_='text').get_text(strip=True)
                author = block.find('small', class_='author').get_text(strip=True)
                
                all_scraped_data.append({
                    "source_url": url,
                    "user": author,
                    "comment_text": text
                })

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        print("Closing WebDriver...")
        driver.quit()

    # 6. Save the AI dataset
    if all_scraped_data:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_scraped_data, f, ensure_ascii=False, indent=4)
        print(f"✅ DONE! Saved {len(all_scraped_data)} user comments/quotes to {output_file}")

if __name__ == "__main__":
    OUTPUT_FILENAME = "ai_test_dataset.json"
    scrape_dummy_dataset(OUTPUT_FILENAME)