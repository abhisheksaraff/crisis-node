# Updated imports for 2026 SDK
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from src.services.ibm_watson_service import API_KEY, PROJECT_ID, URL

# 1. Setup Credentials object correctly
creds = Credentials(
    api_key=API_KEY,
    url=URL
)

# 2. Use ModelInference (The modern way)
model = ModelInference(
    model_id="ibm/granite-3-2-8b-instruct", 
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 500,
        "temperature": 0.2
    },
    credentials=creds,
    project_id=PROJECT_ID
)

def run_crisis_node(report):
    # Fixed syntax for the model call
    return model.generate_text(prompt=report)

if __name__ == "__main__":
    scenario = "Flash flood in Northern Lahore; 50 families stranded."
    print("\n🚨 CRISISNODE ACTIVATED\n")
    print(run_crisis_node(scenario))