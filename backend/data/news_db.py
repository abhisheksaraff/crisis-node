import os
import hashlib
import time
from typing import Optional, Dict, Any, List, cast
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client
from pydantic import BaseModel, Field
from app.schemas.news import NewsEntry

# Setup
load_dotenv(find_dotenv())
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def _generate_id(unique_string: str) -> str:
    """Generates a unique ID from a string (like a URL) to prevent duplicates."""
    return hashlib.md5(unique_string.encode("utf-8")).hexdigest()

def create_news(data: dict):
    """Saves news to 'news' table using exact NewsEntry model."""
    client = get_client()
    
    # Validate using the model to ensure strict adherence to your schema
    entry = NewsEntry(**data)
    payload = entry.model_dump()
    
    # Generate the primary key ID from the link
    payload["id"] = _generate_id(payload["link"])

    try:
        return client.table("news").upsert(payload).execute()
    except Exception as e:
        return {"error": str(e)}

def read_news(limit: int = 100, unread_only: bool = True):
    """Fetches news articles from 'news' table ordered by timestamp."""
    client = get_client()
    query = client.table("news").select("*")
    
    if unread_only:
        query = query.eq("is_read", False)
        
    return query.order("timestamp", desc=True).limit(limit).execute().data

def update_news(news_id: str, update_data: dict):
    """Updates a specific row in 'news' table with Mypy type safety."""
    client = get_client()
    try:
        safe_data = cast(Dict[str, Any], update_data)
        return (
            client.table("news")
            .update(safe_data)
            .eq("id", news_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}

def update_news_location(news_id: str, location_name: str, lat: float, lon: float):
    """Updates the location JSONB field in 'news' table."""
    client = get_client()
    location_payload: Dict[str, Any] = {
        "location": {
            "name": location_name,
            "lat": lat,
            "lon": lon
        }
    }
    try:
        return (
            client.table("news")
            .update(location_payload)
            .eq("id", news_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}

def mark_news_read(news_id: str):
    """Sets is_read = True in 'news' table."""
    client = get_client()
    return client.table("news").update({"is_read": True}).eq("id", news_id).execute()

def delete_all_news():
    """Wipes the 'news' table."""
    client = get_client()
    return client.table("news").delete().neq("id", "0").execute()