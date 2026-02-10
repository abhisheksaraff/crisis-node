import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
from app.db.news_db import update_news_location_type, read_news

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- FUNCTION 1: DATA PREPARATION ---
def build_analysis_prompt(news_items: List[Dict[str, Any]]) -> str:
    """
    Constructs the prompt including event, description, content, and link.
    """
    # Preparing data with the exact fields requested
    lean_data = [
        {
            "id": n["id"],
            "event": n.get("event", "unknown"),
            "description": n.get("description", ""),
            "content": (n.get("content") or "")[:1500],
            "link": n.get("link", "")
        } for n in news_items
    ]

    return f"""
    Analyze these {len(lean_data)} items. 
    1. Verify if 'event' is a real physical disaster.
    2. Set type to 'disaster', 'false_alert', or 'news'.
    3. Extract location {{name, lat, lon}}.
    
    Return ONLY a JSON array of objects:
    [{{"id": "...", "type": "...", "location": {{"name": "...", "lat": 0.0, "lon": 0.0}}}}]

    DATA:
    {json.dumps(lean_data)}
    """

# --- FUNCTION 2: AI INTERACTION ---
async def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Handles the actual API call with basic error catching.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        return response.text
    except Exception as e:
        print(f"API Call Failed: {e}")
        return None

# --- FUNCTION 3: ORCHESTRATOR ---
async def process_batch_with_gemini(limit: int = 40):
    # 1. Get Data
    news = read_news(limit=limit, unread_only=True)
    if not news:
        return {"status": "idle"}

    # 2. Build Prompt
    prompt = build_analysis_prompt(news)
    
    # 3. Call AI
    raw_response = await call_gemini_api(prompt)
    if not raw_response:
        return {"status": "error", "message": "API error or 429 quota hit"}

    # 4. Parse & Update DB
    try:
        decisions = json.loads(raw_response)
        for d in decisions:
            update_news_location_type(
                news_id=d["id"],
                news_type=d["type"],
                location_name=d["location"]["name"],
                lat=d["location"]["lat"],
                lon=d["location"]["lon"]
            )
        return {"status": "success", "count": len(decisions)}
    except json.JSONDecodeError:
        print("AI response was not valid JSON.")
        return {"status": "error"}

# if __name__ == "__main__":
#     asyncio.run(process_batch_with_gemini(limit=5))