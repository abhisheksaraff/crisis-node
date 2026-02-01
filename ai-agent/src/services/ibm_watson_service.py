import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

API_KEY = os.getenv("IBM_WATSONX_API_KEY")
PROJECT_ID = os.getenv("IBM_WATSONX_PROJECT_ID")
URL = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
