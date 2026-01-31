from gnews import GNews
from app.schemas.news import NewsEntry
import json

import nltk
from googlenewsdecoder import gnewsdecoder
from newspaper import Article, Config

# Initialization for the NLTK tokenizer
nltk.download('punkt', quiet=True)

def fetch_article_content(url: str) -> dict:
    """
    Decodes a Google News URL and extracts the full article text and metadata.
    Returns a dictionary with title, text, and real_url.
    """
    final_url = url
    
    # Handle Google News Encoding
    if "news.google.com" in url:
        try:
            decoded = gnewsdecoder(url)
            if decoded.get("status"):
                final_url = decoded["decoded_url"]
        except Exception as e:
            print(f"Decode failed, trying original URL: {e}")

    # Setup Newspaper Config
    config = Config()
    config.browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    config.request_timeout = 15

    # Scrape Article
    article = Article(final_url, config=config)
    try:
        article.download()
        article.parse()
        
        return {
            "title": article.title,
            "text": article.text,
            "url": final_url,
            "authors": article.authors,
            "published": str(article.publish_date)
        }
    except Exception as e:
        print(f"Scraping error for {final_url}: {e}")
        return {"title": "Error", "text": "", "url": final_url}

def scraper_wrapper():
    """This function acts as the bridge between the timer and scraper."""
    print("Background Task: Starting news scrape...")
    try:
        run_scraper() 
        print("Background Task: News saved to JSON.")
    except Exception as e:
        print(f"Background Task Error: {e}")
    
def run_scraper():
    google_news = GNews(language='en', period='12h', max_results=1, proxy=None)
    #google_news = GNews(language='en', period='12h', max_results=15, proxy=None)
    
    keywords = ['flood', 'earthquake', 'wildfire', 'cyclone']
    collected_data = []

    print("Starting disaster scrapers...")

    for query in keywords:
        print(f"Searching Google News for: {query}")
        results = google_news.get_news(query)
        
        for article in results:
            try:
                print(f"Processing: {article.get('title', 'Unknown')[:50]}...")
                
                article_data = fetch_article_content(article['url'])
                full_text_string = article_data.get("text", "") # Get just the text part
        
                # Fallback logic
                if not full_text_string or len(full_text_string) < 50:
                    full_text_string = article.get('description', "No content available.")

                # Ensure everything is a string for Pydantic
                entry = NewsEntry(
                    event=str(query),
                    title=str(article.get('title', 'No Title')),
                    description=str(article.get('description', '')),
                    content=str(full_text_string), 
                    link=str(article.get('url', '')),
                    published=str(article.get('published date', ''))
                )
                collected_data.append(entry)

            except Exception as e:
                # Skip this specific article if it causes any error
                print(f"Skipping article due to error: {e}")
                continue 

    # Export to JSON
    try:
        with open('news.json', 'w') as f:
            json_data = [obj.model_dump() for obj in collected_data]
            json.dump(json_data, f, indent=4)
        print(f"Success {len(collected_data)} articles saved.")
    except Exception as e:
        print(f"Critical JSON Export Error: {e}")
    
    print(f"Success {len(collected_data)} articles saved to news.json")

if __name__ == "__main__":
    run_scraper()