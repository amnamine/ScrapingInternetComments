import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# --- List of practice URLs ---
urls = [
    "https://quotes.toscrape.com/",
    "http://books.toscrape.com/",
    "https://quotes.toscrape.com/tag/humor/",
    "https://quotes.toscrape.com/scroll",
    "https://toscrape.com/",
    "https://www.scrapethissite.com/pages/",
    "https://web-scraping.dev/",
    "https://pythonscraping.com/pages/page1.html",
    "https://pythonscraping.com/pages/page3.html",
    "https://example.com/",
    "https://www.wikipedia.org/",
    "https://www.python.org/about/help/",
    "https://httpbin.org/html",
    "https://jsonplaceholder.typicode.com/posts"
]

# --- Setup Selenium (Chrome example) ---
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Open CSV for results
output_file = "practice_scraped_dataset.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source_url", "text_content"])  # CSV Columns

    # Iterate through each URL
    for url in urls:
        print(f"Scraping: {url}")
        try:
            driver.get(url)
            time.sleep(3)  # wait to load JS content if any

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # collect text from major blocks
            paragraphs = soup.find_all(["p", "span", "li", "h1", "h2", "h3"])
            for block in paragraphs:
                text = block.get_text(strip=True)
                if len(text) > 20:  # filter out tiny text
                    writer.writerow([url, text])

        except Exception as e:
            print(f"Error on {url}:", e)

driver.quit()
print("Done — dataset saved to", output_file)