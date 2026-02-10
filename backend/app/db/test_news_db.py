import time
from news_db import *

def wait_for_user(step_name: str):
    print(f"\n--- NEXT STEP: {step_name} ---")
    input("Press ENTER to execute...")

def run_test_suite():
    print("Starting News DB Test Suite (Table: news)")

    # 1. Sample JSON data
    sample_json = {
        "event": "earthquake",
        "title": "Another earthquake shakes Great Falls - KRTV",
        "description": "Another earthquake shakes Great Falls KRTV",
        "content": "Many people reported feeling what they believe was a small earthquake on Saturday, January 31, 2026...",
        "link": "https://news.google.com/rss/articles/great-falls-quake-unique-id-123",
        "is_read": False,
        "published": "Sun, 01 Feb 2026 01:57:03 GMT",
        "location": {
            "name": None,
            "lat": None,
            "lon": None
        }
    }

    # 2. CREATE
    wait_for_user("create_news (Upsert)")
    result = create_news(sample_json)
    if hasattr(result, 'data') and result.data:
        target_id = result.data[0]['id']
        print(f"SUCCESS: Entry created. ID: {target_id}")
    else:
        print(f"ERROR: {result}")
        return

    # 3. READ
    wait_for_user("read_news (Verify Retrieval)")
    news_items = read_news(limit=1, unread_only=True)
    if news_items:
        print(f"SUCCESS: Found item in DB: {news_items[0]['title']}")
    else:
        print("FAILURE: No items found in DB.")

    # 4. UPDATE LOCATION
    wait_for_user("update_news_location (Great Falls coordinates)")
    update_news_location(target_id, "Great Falls, MT", 47.5053, -111.3008)
    print("SUCCESS: Location updated.")

    # 5. MARK READ
    wait_for_user("mark_news_read")
    mark_news_read(target_id)
    print("SUCCESS: Entry marked as read.")

    # 6. DELETE
    wait_for_user("delete_all_news (Cleanup)")
    delete_all_news()
    print("SUCCESS: 'news' table wiped.")

    print("\nAll tests finished.")

if __name__ == "__main__":
    run_test_suite()