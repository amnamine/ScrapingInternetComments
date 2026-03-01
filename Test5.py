import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Forcing standard output for Windows to prevent emoji/character crashes
sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 1. THE PLATFORM-LEVEL ENGINES
# ==========================================

def parse_stack_exchange(soup, url):
    """Extracts answers and comments from ANY Stack Exchange network site."""
    comments = []
    # Grab answer bodies and comment text
    posts = soup.find_all('div', class_='s-prose js-post-body')
    for post in posts:
        text = post.get_text(separator=' ', strip=True)
        if len(text) > 30:
            comments.append({"source": url, "platform": "StackExchange", "text": text})
            
    comment_blocks = soup.find_all('span', class_='comment-copy')
    for block in comment_blocks:
        text = block.get_text(separator=' ', strip=True)
        if text:
            comments.append({"source": url, "platform": "StackExchange_Comment", "text": text})
    return comments

def parse_discourse_forum(soup, url):
    """Extracts posts from ANY forum running Discourse software."""
    comments = []
    posts = soup.find_all('div', class_='cooked')
    for post in posts:
        text = post.get_text(separator=' ', strip=True)
        if len(text) > 20:
            comments.append({"source": url, "platform": "Discourse", "text": text})
    return comments

def parse_fandom_wiki(soup, url):
    """Extracts lore/text from ANY Fandom/Wikia site."""
    comments = []
    content = soup.find('div', class_='mw-parser-output')
    if content:
        paragraphs = content.find_all('p')
        for p in paragraphs:
            text = p.get_text(separator=' ', strip=True)
            if len(text) > 50:
                comments.append({"source": url, "platform": "FandomWiki", "text": text})
    return comments

def parse_wikipedia_talk(soup, url):
    """Extracts debate comments from Wikipedia Talk pages."""
    comments = []
    content_div = soup.find('div', class_='mw-parser-output')
    if content_div:
        paragraphs = content_div.find_all(['p', 'dd'])
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 40:
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

# ==========================================
# 2. THE MASTER ROUTER
# ==========================================

def run_colossal_scraper(url_list, output_file):
    print("/// INITIALIZING COLOSSAL MULTI-DOMAIN SCRAPER !!! ///")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    massive_dataset = []

    try:
        for idx, url in enumerate(url_list, 1):
            print(f"[{idx}/{len(url_list)}] SCRAPING: {url} ...")
            try:
                driver.get(url)
                # Wait 3 seconds for dynamic JS frameworks (like Discourse) to render
                time.sleep(3) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                extracted_data = []

                # ROUTER LOGIC based on domain signatures
                if "stackexchange.com" in url or "stackoverflow.com" in url or "askubuntu.com" in url or "superuser.com" in url or "serverfault.com" in url:
                    extracted_data = parse_stack_exchange(soup, url)
                elif "discuss." in url or "forums." in url or "users.rust-lang.org" in url or "meta.discourse.org" in url:
                    extracted_data = parse_discourse_forum(soup, url)
                elif "fandom.com" in url:
                    extracted_data = parse_fandom_wiki(soup, url)
                elif "wikipedia.org" in url:
                    extracted_data = parse_wikipedia_talk(soup, url)
                elif "news.ycombinator.com" in url:
                    extracted_data = parse_hackernews(soup, url)
                else:
                    print(f"  -> WARNING: No parser matched for this domain. Skipping.")
                    continue

                if extracted_data:
                    print(f"  -> SUCCESS: Ripped {len(extracted_data)} data blocks.")
                    massive_dataset.extend(extracted_data)
                else:
                    print("  -> FAILED: No data found (Layout might be different or page empty).")

            except Exception as e:
                print(f"  -> ERROR on {url}: {e}")

    finally:
        print("/// CLOSING SELENIUM WEBDRIVER... ///")
        driver.quit()

    if massive_dataset:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(massive_dataset, f, ensure_ascii=False, indent=4)
        print(f"\nBOOM !!! SAVED A MASSIVE TOTAL OF {len(massive_dataset)} COMMENTS/TEXT BLOCKS TO {output_file} !!!")

# ==========================================
# 3. THE COLOSSAL LIST OF URLS (DIFFERENT SITES!)
# ==========================================

if __name__ == "__main__":
    COLOSSAL_URL_LIST = [
        # --- STACK EXCHANGE NETWORK (Different Domains, Same HTML) ---
        "https://stackoverflow.com/questions/11227809/why-is-processing-a-sorted-array-faster-than-processing-an-unsorted-array",
        "https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git",
        "https://stackoverflow.com/questions/200000/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment",
        "https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python",
        "https://superuser.com/questions/163818/how-to-install-a-font-on-windows",
        "https://superuser.com/questions/273756/how-to-change-default-program-for-a-specific-file-extension-in-windows-7",
        "https://askubuntu.com/questions/140246/how-do-i-resolve-unmet-dependencies-after-adding-a-ppa",
        "https://askubuntu.com/questions/222348/what-does-sudo-apt-get-update-do",
        "https://serverfault.com/questions/208522/what-is-strict-transport-security-and-how-do-i-use-it",
        "https://physics.stackexchange.com/questions/2239/what-is-the-speed-of-gravity",
        "https://math.stackexchange.com/questions/733754/visually-stunning-math-concepts-which-are-easy-to-explain",
        "https://english.stackexchange.com/questions/1180/when-to-use-i-e-and-e-g",

        # --- DISCOURSE FORUMS (Different Domains, Same HTML) ---
        "https://meta.discourse.org/t/what-is-discourse/1500",
        "https://meta.discourse.org/t/how-to-start-a-new-topic/1600",
        "https://discuss.python.org/t/pep-703-making-the-global-interpreter-lock-optional-in-cpython/22000",
        "https://discuss.python.org/t/what-is-the-future-of-python-packaging/15000",
        "https://users.rust-lang.org/t/what-is-the-best-way-to-learn-rust/50000",
        "https://users.rust-lang.org/t/understanding-lifetimes-in-rust/40000",
        "https://discuss.pytorch.org/t/what-is-the-difference-between-view-and-reshape/10000",
        "https://discuss.huggingface.co/t/how-to-fine-tune-a-model-on-custom-data/2000",
        "https://forums.fast.ai/t/what-is-the-best-gpu-for-deep-learning/30000",
        "https://forums.docker.com/t/docker-container-exits-immediately-after-starting/10000",

        # --- FANDOM WIKIS (Different Domains, Same HTML - Huge Text Data) ---
        "https://starwars.fandom.com/wiki/Darth_Vader",
        "https://starwars.fandom.com/wiki/Luke_Skywalker",
        "https://starwars.fandom.com/wiki/Jedi",
        "https://marvel.fandom.com/wiki/Peter_Parker_(Earth-616)",
        "https://marvel.fandom.com/wiki/Tony_Stark_(Earth-616)",
        "https://harrypotter.fandom.com/wiki/Harry_Potter",
        "https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
        "https://memory-alpha.fandom.com/wiki/James_T._Kirk",
        "https://memory-alpha.fandom.com/wiki/United_Federation_of_Planets",
        "https://tardis.fandom.com/wiki/The_Doctor",

        # --- WIKIPEDIA TALK PAGES (Different Topics, Same HTML) ---
        "https://en.wikipedia.org/wiki/Talk:History_of_the_world",
        "https://en.wikipedia.org/wiki/Talk:World_War_II",
        "https://en.wikipedia.org/wiki/Talk:Climate_change",
        "https://en.wikipedia.org/wiki/Talk:Quantum_mechanics",
        "https://en.wikipedia.org/wiki/Talk:Theory_of_relativity",
        "https://en.wikipedia.org/wiki/Talk:Evolution",
        "https://en.wikipedia.org/wiki/Talk:Dinosaurs",
        "https://en.wikipedia.org/wiki/Talk:Space_exploration",
        "https://en.wikipedia.org/wiki/Talk:Solar_System",
        "https://en.wikipedia.org/wiki/Talk:Black_hole",
        "https://en.wikipedia.org/wiki/Talk:Mathematics",
        "https://en.wikipedia.org/wiki/Talk:Philosophy",
        "https://en.wikipedia.org/wiki/Talk:Psychology",
        "https://en.wikipedia.org/wiki/Talk:Economics",
        "https://en.wikipedia.org/wiki/Talk:Politics",

        # --- HACKER NEWS (Different Items, Same HTML) ---
        "https://news.ycombinator.com/item?id=38200000",
        "https://news.ycombinator.com/item?id=38201000",
        "https://news.ycombinator.com/item?id=38202000",
        "https://news.ycombinator.com/item?id=38203000",
        "https://news.ycombinator.com/item?id=38204000",
        "https://news.ycombinator.com/item?id=38205000",
        "https://news.ycombinator.com/item?id=38206000",
        "https://news.ycombinator.com/item?id=38207000",
        "https://news.ycombinator.com/item?id=38208000",
        "https://news.ycombinator.com/item?id=38209000",
        "https://news.ycombinator.com/item?id=38210000",
        "https://news.ycombinator.com/item?id=38211000"
    ]
    
    OUTPUT_FILE = "colossal_multi_platform_dataset.json"
    
    run_colossal_scraper(COLOSSAL_URL_LIST, OUTPUT_FILE)