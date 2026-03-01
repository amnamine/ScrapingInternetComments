import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Fix for Windows console printing errors - forcing standard output
sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 1. THE DOMAIN-SPECIFIC PARSERS
# ==========================================

def parse_wikipedia_talk(soup, url):
    """Extracts debate comments from Wikipedia Talk pages."""
    comments = []
    content_div = soup.find('div', class_='mw-parser-output')
    if content_div:
        paragraphs = content_div.find_all(['p', 'dd'])
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 60: # Only get substantial comments
                comments.append({"source": url, "platform": "Wikipedia", "text": text})
    return comments

def parse_hackernews(soup, url):
    """Extracts comments from Hacker News threads."""
    comments = []
    comment_spans = soup.find_all('div', class_='commtext')
    for span in comment_spans:
        text = span.get_text(separator=' ', strip=True)
        if text:
            comments.append({"source": url, "platform": "HackerNews", "text": text})
    return comments

def parse_github_issues(soup, url):
    """Extracts developer comments from public GitHub Issues."""
    comments = []
    comment_bodies = soup.find_all('td', class_='comment-body')
    for body in comment_bodies:
        text = body.get_text(separator=' ', strip=True)
        if text and len(text) > 20:
            comments.append({"source": url, "platform": "GitHub", "text": text})
    return comments

def parse_dummy_quotes(soup, url):
    """Extracts text from the open scraping sandbox."""
    comments = []
    blocks = soup.find_all('div', class_='quote')
    for block in blocks:
        text_element = block.find('span', class_='text')
        if text_element:
            comments.append({"source": url, "platform": "ScrapeSandbox", "text": text_element.get_text(strip=True)})
    return comments

# ==========================================
# 2. THE MASTER SELENIUM ROUTER
# ==========================================

def run_massive_selenium_scraper(url_list, output_file):
    print("INITIALIZING MASSIVE SELENIUM SCRAPER...")
    
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
            print(f"SCRAPING: {url} ...")
            try:
                driver.get(url)
                # Give Selenium time to render JavaScript and HTML
                time.sleep(3) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                extracted_data = []

                # ROUTER LOGIC: Route to the correct parser based on the URL domain
                if "wikipedia.org" in url:
                    extracted_data = parse_wikipedia_talk(soup, url)
                elif "news.ycombinator.com" in url:
                    extracted_data = parse_hackernews(soup, url)
                elif "github.com" in url:
                    extracted_data = parse_github_issues(soup, url)
                elif "toscrape.com" in url:
                    extracted_data = parse_dummy_quotes(soup, url)
                else:
                    print(f"  -> No parser built for this domain. Skipping.")
                    continue

                if extracted_data:
                    print(f"  -> SUCCESS: Extracted {len(extracted_data)} comments.")
                    massive_dataset.extend(extracted_data)
                else:
                    print("  -> WARNING: No comments found. Page might be empty or layout changed.")

            except Exception as e:
                print(f"  -> ERROR on {url}: {e}")

    finally:
        print("CLOSING SELENIUM WEBDRIVER...")
        driver.quit()

    if massive_dataset:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(massive_dataset, f, ensure_ascii=False, indent=4)
        print(f"DONE! Saved a total of {len(massive_dataset)} comments to {output_file}!")

# ==========================================
# 3. THE MASSIVE LIST OF 40+ URLS !!!
# ==========================================

if __name__ == "__main__":
    MASSIVE_URL_LIST = [
        # WIKIPEDIA TALK PAGES (Massive text debates)
        "https://en.wikipedia.org/wiki/Talk:Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Talk:Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Talk:Web_scraping",
        "https://en.wikipedia.org/wiki/Talk:Machine_learning",
        "https://en.wikipedia.org/wiki/Talk:Internet",
        "https://en.wikipedia.org/wiki/Talk:Computer_science",
        "https://en.wikipedia.org/wiki/Talk:Algorithm",
        "https://en.wikipedia.org/wiki/Talk:Data_science",
        "https://en.wikipedia.org/wiki/Talk:Deep_learning",
        "https://en.wikipedia.org/wiki/Talk:Neural_network",

        # HACKER NEWS THREADS (Tech discussions)
        "https://news.ycombinator.com/item?id=38201931",
        "https://news.ycombinator.com/item?id=38202100",
        "https://news.ycombinator.com/item?id=38199500",
        "https://news.ycombinator.com/item?id=38198422",
        "https://news.ycombinator.com/item?id=38197000",
        "https://news.ycombinator.com/item?id=38196000",
        "https://news.ycombinator.com/item?id=38195000",
        "https://news.ycombinator.com/item?id=38194000",
        "https://news.ycombinator.com/item?id=38193000",
        "https://news.ycombinator.com/item?id=38192000",

        # GITHUB PUBLIC ISSUES (Developer comments)
        "https://github.com/python/cpython/issues/100000",
        "https://github.com/python/cpython/issues/100001",
        "https://github.com/python/cpython/issues/100002",
        "https://github.com/facebook/react/issues/28200",
        "https://github.com/facebook/react/issues/28201",
        "https://github.com/facebook/react/issues/28202",
        "https://github.com/microsoft/vscode/issues/200000",
        "https://github.com/microsoft/vscode/issues/200001",
        "https://github.com/microsoft/vscode/issues/200002",
        "https://github.com/microsoft/vscode/issues/200003",

        # DUMMY SANDBOX PAGES (Clean text extraction)
        "http://quotes.toscrape.com/page/1/",
        "http://quotes.toscrape.com/page/2/",
        "http://quotes.toscrape.com/page/3/",
        "http://quotes.toscrape.com/page/4/",
        "http://quotes.toscrape.com/page/5/",
        "http://quotes.toscrape.com/page/6/",
        "http://quotes.toscrape.com/page/7/",
        "http://quotes.toscrape.com/page/8/",
        "http://quotes.toscrape.com/page/9/",
        "http://quotes.toscrape.com/page/10/"
    ]
    
    OUTPUT_FILE = "massive_selenium_dataset.json"
    
    run_massive_selenium_scraper(MASSIVE_URL_LIST, OUTPUT_FILE)