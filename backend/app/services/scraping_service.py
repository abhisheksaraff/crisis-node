from gnews import GNews
import json

def scraper_wrapper():
    """This function acts as the bridge between the timer and your scraper."""
    print("Background Task: Starting news scrape...")
    try:
        run_scraper() 
        print("Background Task: News saved to JSON for NLP partner.")
    except Exception as e:
        print(f"Background Task Error: {e}")

def run_scraper():
    google_news = GNews(language='en', period='12h', max_results=15) # 1. Setup GNews (Last 12 hours)
    
    keywords = ['flood', 'earthquake', 'wildfire', 'cyclone']
    #japanese_keywords = ['洪水', '地震', '山火事', 'サイクロン']
    collected_data = []

    print("Starting disaster scrapers...")

    for query in keywords:
        print(f"Searching Google News for: {query}")
        results = google_news.get_news(query)
        for article in results:
            # Structuring the data for your NLP partner
            entry = {
                "source_keyword": query,
                "title": article['title'],
                "description": article['description'],
                "link": article['url'],
                "published": article['published date']
            }
            collected_data.append(entry)

    #Export to JSON
    with open('news_handoff.json', 'w') as f:
        json.dump(collected_data, f, indent=4)
    
    print(f"Success {len(collected_data)} articles saved to news_handoff.json")

if __name__ == "__main__":
    run_scraper()