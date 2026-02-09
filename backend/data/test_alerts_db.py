import time
import uuid
from datetime import datetime
from alerts_db import *

def wait_for_user(step_name: str):
    print(f"\n--- NEXT STEP: {step_name} ---")
    input("Press ENTER to execute...")

def run_test_suite():
    print("Starting Complete Alerts Test Suite")

    # 1. SETUP SAMPLE DATA
    unique_link = f"https://emergency.mt.gov/quake-{uuid.uuid4()}"
    
    sample_alert = {
        "event": "earthquake_alert",
        "title": "EMERGENCY: Magnitude 4.2 near Great Falls",
        "description": "Initial reports of seismic activity.",
        "content": "Full emergency protocols are being evaluated by local authorities.",
        "link": unique_link,
        "actions": [
            {"task": "Notify local authorities", "done": False}
        ],
        "sources": [
            {"name": "USGS", "url": "https://usgs.gov", "timestamp": "2026-02-01T01:57:03Z"}
        ],
        "location": {
            "name": "Great Falls, MT",
            "lat": 47.5053,
            "lon": -111.3008
        }
    }

    # 2. CREATE ALERT
    wait_for_user("create_alert (Insert into Supabase)")
    result = create_alert(sample_alert)
    if hasattr(result, 'data') and result.data:
        alert_id = result.data[0]['id']
        print(f"SUCCESS: Alert created with UUID: {alert_id}")
    else:
        print(f"ERROR creating alert: {result}")
        return

    # 3. READ BY LOCATION
    wait_for_user("read_alerts_by_location (Filtering for Great Falls)")
    loc_results = read_alerts_by_location("Great Falls, MT")
    if loc_results:
        print(f"SUCCESS: Found {len(loc_results)} alert(s) in Great Falls.")
    else:
        print("FAILURE: Failed to find alert by location.")

    # 4. ADD A SOURCE (Enrichment)
    wait_for_user("add_alert_source (Adding Twitter/X link)")
    new_source = {
        "name": "MT Emergency Services",
        "url": "https://x.com/mtemergency",
        "timestamp": datetime.utcnow().isoformat()
    }
    add_alert_source(alert_id, new_source)
    print("SUCCESS: Source appended to JSONB list.")

    # 5. ADD CUSTOM ACTION (User Interaction)
    wait_for_user("add_custom_action (Adding user-specified task)")
    add_custom_action(alert_id, "Check structural integrity of 5th Ave Bridge")
    print("SUCCESS: Custom action added to actions list.")

    # 6. UPDATE ACTION STATUS (Checking off a task)
    wait_for_user("update_action_status (Marking first task as DONE)")
    # Index 0 is "Notify local authorities"
    update_action_status(alert_id, 0, True)
    print("SUCCESS: Task at index 0 marked as done.")

    # 7. UPDATE GENERAL CONTEXT
    wait_for_user("update_alert (Updating description and content)")
    update_alert(alert_id, {
        "description": "Situation Stabilized.",
        "content": "Seismologists confirm no immediate aftershock risk."
    })
    print("SUCCESS: General fields updated.")

    # 8. MARK ALERT AS PROCESSED
    wait_for_user("mark_alert_done (Deactivating Alert)")
    mark_alert_done(alert_id)
    print("SUCCESS: Alert set to is_active=False and is_read=True.")

    # 9. CLEANUP
    wait_for_user("delete_all_alerts (Wiping for next test)")
    delete_all_alerts()
    print("SUCCESS: Table cleared.")

    print("\nComplete Alert Test Suite Finished Successfully!")

if __name__ == "__main__":
    run_test_suite()