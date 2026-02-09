import sys, time
from pathlib import Path

# Move up to the crisis-node root
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

# Add the backend folder to find schemas
sys.path.insert(0, str(root / "backend"))

from data.db import *

def get_pending_news(limit: int = 10):
    """Specific helper to find news that hasn't been processed."""
    return read_news(limit=limit, unread_only=True)

async def process_pending_batch():
    """Iterates through unread news and enriches them."""
    # 1. Fetch a small batch of work
    pending_items = read_news(limit= 5, unread_only= True)
    results = []

    if not pending_items:
        return {"status": "idle", "message": "No news to process"}

    for item in pending_items:
        try:
            # logic for watsonx.ai extraction
            # location = call_watsonx_ai(item['text'])
            location = "Extracted Location" # Placeholder
            
            # Update the specific document
            update_news(item['_id'], {
                "location": location,
                "is_read": True, # Mark as processed
                "status": "enriched"
            })
            
            results.append({"id": item['_id'], "status": "success"})
            
        except Exception as e:
            results.append({"id": item['_id'], "status": "failed", "error": str(e)})

    return {"processed_count": len(results), "details": results}