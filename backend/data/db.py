import os
import hashlib
from typing import List, Optional
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client
import uuid

# Setup
load_dotenv(find_dotenv())
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Private Utils
def _generate_id(unique_string: str):
    """Generates a unique ID from a string (like a URL) to prevent duplicates."""
    return hashlib.md5(unique_string.encode("utf-8")).hexdigest()

#-------------- News Starts --------------------

def create_news(data: dict):
    """
    Saves news to Supabase news_entries table.
    Uses .upsert() to handle duplicates based on the ID automatically.
    """
    client = get_client()
    
    if "link" in data:
        data["id"] = _generate_id(data["link"])

    try:
        # upsert checks the primary key (id). 
        # If it exists, it updates; if not, it inserts.
        return client.table("news").upsert(data).execute()
    except Exception as e:
        return {"error": str(e)}

def read_news(limit: int = 100, unread_only: Optional[bool] = None):
    """
    Fetches news articles from news_entries.
    """
    client = get_client()
    query = client.table("news").select("*")
    
    if unread_only is True:
        query = query.eq("is_read", False)
    elif unread_only is False:
        query = query.eq("is_read", True)
        
    # Order by timestamp descending and apply limit
    return query.order("timestamp", desc=True).limit(limit).execute().data

def update_news(doc_id: str, update_data: dict):
    """Updates a specific row by its ID."""
    client = get_client()
    return client.table("news").update(update_data).eq("id", doc_id).execute()

def mark_news_read(news_id: str):
    """
    Updates a news entry to set is_read = True.
    """
    client = get_client()
    try:
        return (
            client.table("news")
            .update({"is_read": True})
            .eq("id", news_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}

def delete_news(doc_id: str):
    """Deletes a row. No revision ID required in Supabase."""
    client = get_client()
    return client.table("news").delete().eq("id", doc_id).execute()

def delete_all_news():
    """
    Deletes all rows from the news table.
    """
    client = get_client()
    try:
        # Using .neq("id", "0") or .not_.is_("id", "null") acts as a "select all"
        return client.table("news").delete().neq("id", "0").execute()
    except Exception as e:
        return {"error": str(e)}
    
#-------------- News Ends --------------------

#-------------- Alerts Starts --------------------

class AlertService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table = "alerts"

    def create_alert(self, alert: AlertEntry) -> dict:
        """Inserts a new verified alert into the database."""
        # .model_dump(mode='json') converts Python objects/datetimes to JSON strings
        data = alert.model_dump(exclude_none=True, mode='json')
        response = self.supabase.table(self.table).insert(data).execute()
        return response.data[0]

    def get_active_alerts(self, city: Optional[str] = None) -> List[dict]:
        """Fetches all active alerts, optionally filtered by city."""
        query = self.supabase.table(self.table).select("*").eq("is_active", True)
        if city:
            query = query.eq("location->>name", city) # Filters inside JSONB
        response = query.execute()
        return response.data

    def update_alert(self, alert_id: str, updates: dict) -> dict:
        """
        Updates an existing alert. 
        If updating actions/sources, ensure you pass the full list.
        """
        updates["updated_at"] = "now()" # Let Postgres handle the timestamp
        response = self.supabase.table(self.table).update(updates).eq("id", alert_id).execute()
        return response.data[0]

    def mark_as_read(self, alert_id: str):
        """Standard 'Read' toggle for the frontend."""
        return self.update_alert(alert_id, {"is_read": True})

    def delete_alert(self, alert_id: str):
        """Permanent deletion of an alert."""
        return self.supabase.table(self.table).delete().eq("id", alert_id).execute()
    
#-------------- Alerts Ends --------------------

# import time
# from app.schemas.news import NewsEntry

# # The sample data provided
# sample_data = {
#     "event": "earthquake",
#     "title": "Another earthquake shakes Great Falls - KRTV",
#     "description": "Another earthquake shakes Great Falls KRTV",
#     "content": "Many people reported feeling what they believe was a small earthquake on Saturday, January 31, 2026...",
#     "link": "https://news.google.com/rss/articles/CBMikAFBVV95cUxOQl9YZkZoLUpNMUIyMVl3MXIyMzRfa0ozMUJodTc0MVJMNEhNWG0zenBJcWtfZzZCa3pzb2pfdklkQzZSa1dtbnBqb0dxMXR3Yy1OQXZ2OFN4aTVhWWtJbFlCRGJ4VzB3Ukw4U0tCeUJjYUx3YWlVcWR3a0NxdjNNOUdwQmhZRUp6YWJGSHppZFo?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
#     "is_read": False,
#     "published": "Sun, 01 Feb 2026 01:57:03 GMT",
#     "type": "news",
#     "timestamp": time.time(),
#     "location": {
#         "name": "Great Falls",
#         "lat": 47.5053,
#         "lon": -111.3008
#     }
# }

# def run_test():
#     try:
#         entry = NewsEntry(**sample_data)
#         result = create_news(entry.model_dump())
        
#         # Check if result is the Supabase response object or an error dict
#         if hasattr(result, 'data'):
#             print("Successfully inserted news!")
#             print(f"Generated ID: {result.data[0]['id']}")
#         else:
#             print(f"Insertion failed or returned unexpected format: {result}")
        
#     except Exception as e:
#         print(f"Test failed: {e}")

# def test_read():
#     print("--- Fetching Unread News ---")
#     # This calls the function we wrote earlier
#     unread_news = read_news(limit=5, unread_only=True)
    
#     if unread_news:
#         for article in unread_news:
#             print(article)
#             print("-" * 20)
#     else:
#         print("No unread news found.")

# if __name__ == "__main__":
#     test_read()