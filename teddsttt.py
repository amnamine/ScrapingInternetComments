import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_massive_dataset(url_list, output_file):
    """
    Scrapes a massive list of URLs using Selenium and BeautifulSoup.
    Extracts text and author data to build a large AI dataset.
    """
    print("INITIALIZING MASSIVE SCRAPER... !!!!!!!!")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    massive_dataset = []

    try:
        for url in url_list:
            print(f"/// SCRAPING: {url} ...")
            driver.get(url)
            
            # Wait for JS to load
            time.sleep(2) 
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # ---------------------------------------------------------
            # PARSER LOGIC: This matches the structure of the dummy sites
            # ---------------------------------------------------------
            blocks = soup.find_all('div', class_='quote') 
            
            if not blocks:
                print(f"  -> No data found on {url}. Moving to next...")
                continue

            print(f"  -> EXTRACTED {len(blocks)} ITEMS!")
            
            for block in blocks:
                # Extract text and author
                text_element = block.find('span', class_='text')
                author_element = block.find('small', class_='author')
                
                if text_element and author_element:
                    massive_dataset.append({
                        "source_url": url,
                        "user": author_element.get_text(strip=True),
                        "content_text": text_element.get_text(strip=True)
                    })

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        
    finally:
        print("CLOSING WEBDRIVER... ///")
        driver.quit()

    if massive_dataset:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(massive_dataset, f, ensure_ascii=False, indent=4)
        print(f"✅ BOOM! SAVED {len(massive_dataset)} ROWS OF DATA TO {output_file} !!!!!!!!!")

if __name__ == "__main__":
    # MASSIVE LIST OF 35+ URLs READY FOR SCRAPING !!!!!!!!!!
    # These are all legal, open sandbox pages structured identically so the parser works flawlessly.
    HUGE_URL_LIST = [
        "http://quotes.toscrape.com/page/1/",
        "http://quotes.toscrape.com/page/2/",
        "http://quotes.toscrape.com/page/3/",
        "http://quotes.toscrape.com/page/4/",
        "http://quotes.toscrape.com/page/5/",
        "http://quotes.toscrape.com/page/6/",
        "http://quotes.toscrape.com/page/7/",
        "http://quotes.toscrape.com/page/8/",
        "http://quotes.toscrape.com/page/9/",
        "http://quotes.toscrape.com/page/10/",
        "http://quotes.toscrape.com/tag/love/page/1/",
        "http://quotes.toscrape.com/tag/inspirational/page/1/",
        "http://quotes.toscrape.com/tag/life/page/1/",
        "http://quotes.toscrape.com/tag/humor/page/1/",
        "http://quotes.toscrape.com/tag/books/page/1/",
        "http://quotes.toscrape.com/tag/reading/page/1/",
        "http://quotes.toscrape.com/tag/friendship/page/1/",
        "http://quotes.toscrape.com/tag/friends/page/1/",
        "http://quotes.toscrape.com/tag/truth/page/1/",
        "http://quotes.toscrape.com/tag/simile/page/1/",
        "http://quotes.toscrape.com/tag/attributed-no-source/page/1/",
        "http://quotes.toscrape.com/tag/success/page/1/",
        "http://quotes.toscrape.com/tag/philosophy/page/1/",
        "http://quotes.toscrape.com/tag/religion/page/1/",
        "http://quotes.toscrape.com/tag/science/page/1/",
        "http://quotes.toscrape.com/tag/writing/page/1/",
        "http://quotes.toscrape.com/tag/understanding/page/1/",
        "http://quotes.toscrape.com/tag/knowledge/page/1/",
        "http://quotes.toscrape.com/tag/courage/page/1/",
        "http://quotes.toscrape.com/tag/hope/page/1/",
        "http://quotes.toscrape.com/tag/death/page/1/",
        "http://quotes.toscrape.com/tag/romance/page/1/",
        "http://quotes.toscrape.com/tag/music/page/1/",
        "http://quotes.toscrape.com/tag/education/page/1/",
        "http://quotes.toscrape.com/tag/mind/page/1/",
        "http://quotes.toscrape.com/tag/poetry/page/1/"
    ]
    
    OUTPUT_FILE = "massive_ai_dataset.json"
    
    scrape_massive_dataset(HUGE_URL_LIST, OUTPUT_FILE)