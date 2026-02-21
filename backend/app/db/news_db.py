from __future__ import annotations
import os
import hashlib
import time
from typing import Optional, Dict, Any, List, cast
from dotenv import load_dotenv, find_dotenv
from postgrest.exceptions import APIError
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
    """
    Saves news to Supabase news_entries table.
    Uses .upsert() to handle duplicates based on the ID automatically.
    """
    client = get_client()
    
    if "link" in data:
        data["news_id"] = _generate_id(data["link"])

    try:
        # upsert checks the primary key (id). 
        # If it exists, it updates; if not, it inserts.
        return client.table("news").upsert(data).execute()
    except Exception as e:
        return {"error": str(e)}

def read_news(limit: int = 100, unread_only: bool = True):
    """Fetches news articles from 'news' table ordered by timestamp."""
    client = get_client()
    query = client.table("news").select("*")
    
    if unread_only:
        query = query.eq("is_read", False)
        
    return query.order("timestamp", desc=True).limit(limit).execute().data

def get_news_locations(unread_only: bool = False) -> List[str]:
    """
    Fetches unique location names from the news JSONB field.
    Optionally filters by unread status.
    """
    client = get_client()
    
    # Start the query selecting only the location column
    query = client.table("news").select("location")
    
    # Apply filter if unread_only is True
    if unread_only:
        query = query.eq("is_read", False)
        
    response = query.execute()
    data = cast(List[Dict[str, Any]], response.data)
    
    # Extract the "name" field from inside the location JSONB object
    locations = {
        item["location"]["name"] 
        for item in data 
        if item.get("location") 
        and isinstance(item["location"], dict) 
        and "name" in item["location"]
    }
    
    return sorted(list(locations))

def read_news_by_location(location_name: str, limit: int = 50):
    """Fetches news articles for a specific location."""
    client = get_client()
    try:
        return (
            client.table("news")
            .select("*")
            .eq("location->>name", location_name) 
            .execute()
            .data
        )
    except APIError as e:
        # This catches "Column not found" or "Permission denied"
        print(f"Supabase/Postgres Error: {e.message} (Code: {e.code})")
        return []
    except Exception as e:
        # This catches "No internet" or "Python syntax error"
        print(f"General System Error: {e}")
        return []

def update_news(news_id: str, update_data: dict):
    """Updates a specific row in 'news' table with Mypy type safety."""
    client = get_client()
    try:
        safe_data = cast(Dict[str, Any], update_data)
        return (
            client.table("news")
            .update(safe_data)
            .eq("news_id", news_id)
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
            .eq("news_id", news_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}

def update_news_location_type(news_id: str, news_type: str, location_name: str, lat: float, lon: float):
    client = get_client()
    
    # Start with standard payload
    update_payload: Dict[str, Any] = {
        "type": news_type,
        "location": {
            "name": location_name,
            "lat": lat,
            "lon": lon
        },
    }

    # If it's a false alert, mark it as read automatically
    if news_type == "false_alert":
        update_payload["is_read"] = True
    
    try:
        return (
            client.table("news")
            .update(update_payload)
            .eq("news_id", news_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}

def mark_news_read(news_id: str):
    """Sets is_read = True in 'news' table."""
    client = get_client()
    return client.table("news").update({"is_read": True}).eq("news_id", news_id).execute()

def mark_all_news_read():
    """Sets is_read = True for every row in the 'news' table."""
    client = get_client()
    return client.table("news").update({"is_read": True}).neq("is_read", True).execute()

def delete_all_news():
    """Wipes the 'news' table."""
    client = get_client()
    return client.table("news").delete().neq("news_id", "0").execute()