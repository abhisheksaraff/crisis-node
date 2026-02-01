import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient

load_dotenv()

credentials = {
    "url": os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
    "apikey": os.getenv("IBM_WATSONX_API_KEY")
}

print("\n🔍 Connecting to IBM Cloud...")
try:
    client = APIClient(credentials)
    print("✅ Connection Successful! Here are your projects:\n")
    
    client.projects.list(limit=5)
    
except Exception as e:
    print(f"❌ Error: {e}")