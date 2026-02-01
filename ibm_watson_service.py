import os
from ibm_watsonx_ai import APIClient

# --- FINAL VERIFIED CREDENTIALS ---
# Removed the extra dot from the end of the PROJECT_ID
API_KEY = "GvydvXw860wJqVJwijt1gBANsZPbDKjzbXvK6qlU4pb"
PROJECT_ID = "6725ff467feb4ad89377b81cd471de2d" 

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": API_KEY
}

def get_watson_client():
    """Initializes and returns the WatsonX AI Client."""
    try:
        client = APIClient(credentials)
        client.set.default_project(PROJECT_ID)
        print("\n✅ CONNECTION SUCCESSFUL: CrisisNode is now linked to WatsonX AI.")
        return client
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        return None

if __name__ == "__main__":
    get_watson_client()