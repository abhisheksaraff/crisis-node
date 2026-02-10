from __future__ import annotations
import os
from typing import Optional, Dict, Any, List, cast
from postgrest.exceptions import APIError
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client
from pydantic import BaseModel
import json
from backend.app.schemas.alerts import AlertEntry

# Setup
load_dotenv(find_dotenv())
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def create_alert(data: dict):
    """Saves a verified alert to the 'alerts' table."""
    client = get_client()
    
    # 1. Validate using the model
    entry = AlertEntry(**data)
    
    # 2. Convert to JSON-compatible dict (handles UUID and Datetime)
    # We use json.loads(entry.model_dump_json()) to ensure 
    # UUIDs and Datetimes are converted to strings.
    payload = json.loads(entry.model_dump_json(exclude_none=True))

    try:
        # Note: We do NOT generate an ID here; Supabase handles the UUID.
        return client.table("alerts").insert(payload).execute()
    except Exception as e:
        return {"error": str(e)}

def read_alerts(limit: int = 50, active_only: bool = True):
    """Fetches alerts from the 'alerts' table."""
    client = get_client()
    query = client.table("alerts").select("*")
    
    if active_only:
        query = query.eq("is_active", True)
        
    return query.order("created_at", desc=True).limit(limit).execute().data


def get_alert_locations(active_only: bool = True) -> List[str]:
    """
    Returns a unique list of all location names currently in the alerts table.
    Casting 'response.data' to List[Dict[str, Any]] to satisfy Mypy.
    """
    client = get_client()
    query = client.table("alerts").select("location->>name")
    
    if active_only:
        query = query.eq("is_active", True)
        
    response = query.execute()
    data = cast(List[Dict[str, Any]], response.data)
    
    names = {item['name'] for item in data if item.get('name')}
    return sorted(list(names))

def read_alerts_by_location(location_name: str, active_only: bool = True):
    """
    Fetches alerts filtered by the 'name' inside the location JSONB object.
    Gracefully handles database errors to prevent server crashes.
    """
    client = get_client()
    
    # 1. Target the 'name' key inside the 'location' JSONB column
    # ->> extracts the JSON value as text for comparison
    query = client.table("alerts").select("*").eq("location->>name", location_name)
    
    if active_only:
        query = query.eq("is_active", True)
        
    try:
        # 2. Execute and return only the .data list
        response = query.order("created_at", desc=True).execute()
        return response.data
    except APIError as e:
        # Specifically catches Supabase/Postgres errors (like missing columns)
        print(f"Supabase API Error for location '{location_name}': {e.message}")
        return []
    except Exception as e:
        # Catches connection issues or unexpected Python errors
        print(f"Unexpected error in read_alerts_by_location: {e}")
        return []

def update_alert(alert_id: str, update_data: dict):
    """Updates a specific alert by its UUID."""
    client = get_client()
    try:
        safe_data = cast(Dict[str, Any], update_data)
        return (
            client.table("alerts")
            .update(safe_data)
            .eq("id", alert_id)
            .execute()
        )
    except Exception as e:
        return {"error": str(e)}
    
def add_alert_source(alert_id: str, new_source: dict):
    client = get_client()
    
    # Execute the query
    response = client.table("alerts").select("sources").eq("id", alert_id).single().execute()
    
    # 1. Cast the data to a dictionary to fix the .get() error
    # We know .single() returns a dict if successful
    data = cast(Dict[str, Any], response.data)
    
    if not data:
        return {"error": "Alert not found"}

    # 2. Extract and cast the sources list to fix the .append() error
    sources = cast(List[Dict[str, Any]], data.get("sources", []))
    
    # 3. Modify and Update
    sources.append(new_source)
    return client.table("alerts").update({"sources": sources}).eq("id", alert_id).execute()

def update_alert_action_status(alert_id: str, task_index: int, is_done: bool):
    client = get_client()
    response = client.table("alerts").select("actions").eq("id", alert_id).single().execute()
    
    data = cast(Dict[str, Any], response.data)
    if not data:
        return {"error": "Alert not found"}
        
    actions = cast(List[Dict[str, Any]], data.get("actions", []))
    
    if 0 <= task_index < len(actions):
        actions[task_index]["done"] = is_done
        return client.table("alerts").update({"actions": actions}).eq("id", alert_id).execute()
        
    return {"error": "Index out of range"}

def add_custom_action(alert_id: str, task_text: str):
    """
    Adds a custom user-inputted task to the alert actions JSONB list.
    Uses type casting to satisfy Mypy union-attr errors.
    """
    client = get_client()
    
    # 1. Fetch current actions
    response = client.table("alerts").select("actions").eq("id", alert_id).single().execute()
    
    # 2. Cast response data to dict to enable .get()
    data = cast(Dict[str, Any], response.data)
    if not data:
        return {"error": f"Alert with ID {alert_id} not found."}
    
    # 3. Cast the list itself to enable .append()
    actions = cast(List[Dict[str, Any]], data.get("actions", []))
    
    # 4. Modify and update
    actions.append({"task": task_text, "done": False})
    
    return (
        client.table("alerts")
        .update({"actions": actions})
        .eq("id", alert_id)
        .execute()
    )

def mark_alert_done(alert_id: str):
    """Helper to deactivate an alert or mark it read."""
    client = get_client()
    return client.table("alerts").update({"is_active": False, "is_read": True}).eq("id", alert_id).execute()

def delete_all_alerts():
    """Wipes the 'alerts' table."""
    client = get_client()
    return client.table("alerts").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()