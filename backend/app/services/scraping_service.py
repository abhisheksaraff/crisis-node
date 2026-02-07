import json
import nltk
from typing import List
from gnews import GNews
from googlenewsdecoder import gnewsdecoder
from newspaper import Article, Config

from data.db import create_news
from backend.app.schemas.news import NewsEntry

# Initialization for the NLTK tokenizer
nltk.download('punkt', quiet=True)

# --- 1. EXTRACTION LOGIC ---

def fetch_article_content(url: str) -> dict:
    """Decodes Google News URL and extracts full article text/metadata."""
    final_url = url
    if "news.google.com" in url:
        try:
            decoded = gnewsdecoder(url)
            if decoded.get("status"):
                final_url = decoded["decoded_url"]
        except Exception as e:
            print(f"Decode failed for {url}: {e}")

    config = Config()
    config.browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
    config.request_timeout = 15

    article = Article(final_url, config=config)
    try:
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "url": final_url,
            "published": str(article.publish_date)
        }
    except Exception as e:
        print(f"Scraping error: {e}")
        return {"title": "Error", "text": "", "url": final_url}

# --- 2. STORAGE MODULES ---

def save_to_file(entries: List[NewsEntry], filename: str = "news.json"):
    """Saves a list of NewsEntry objects to a local JSON file."""
    try:
        json_data = [obj.model_dump() for obj in entries]
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Successfully saved {len(entries)} articles to {filename}")
    except Exception as e:
        print(f"File Save Error: {e}")

def save_to_database(entries: List[NewsEntry]):
    """Iterates through entries and saves each to Cloudant DB via db.py."""
    count = 0
    for entry in entries:
        try:
            # Convert Pydantic object to dict for Cloudant
            res = create_news(entry.model_dump())
            if res and ("ok" in res or "id" in res):
                count += 1
        except Exception as e:
            print(f"DB Save Error for {entry.title[:30]}: {e}")
    print(f"Successfully synced {count} new articles to Cloudant.")

# --- 3. CORE LOGIC ---

def run_scraper():
    """Main execution logic for scraping news."""
    google_news = GNews(language='en', period='12h', max_results=1)
    keywords = ['flood', 'earthquake', 'wildfire', 'cyclone']
    collected_entries = []

    print("Starting disaster scrapers...")

    for query in keywords:
        print(f"Searching: {query}")
        results = google_news.get_news(query)
        
        for article in results:
            try:
                article_data = fetch_article_content(article['url'])
                full_text = article_data.get("text") or article.get('description', "No content.")

                # Instantiate the Pydantic model
                entry = NewsEntry(
                    event=str(query),
                    title=str(article.get('title', 'No Title')),
                    description=str(article.get('description', '')),
                    content=str(full_text), 
                    link=str(article.get('url', '')),
                    published=str(article.get('published date', ''))
                )
                collected_entries.append(entry)
                print(f"Processed: {entry.title[:50]}...")

            except Exception as e:
                print(f"Skipping article: {e}")
                continue 

    # Modular Storage Calls
    #save_to_file(collected_entries)
    #save_to_database(collected_entries)
    
def scraper_wrapper():
    """This function acts as the bridge between the FastAPI scheduler and the scraper."""
    print("Background Task: Starting news scrape...")
    try:
        run_scraper() 
        print("Background Task: Scrape complete.")
    except Exception as e:
        print(f"Background Task Error: {e}")

if __name__ == "__main__":
    run_scraper()