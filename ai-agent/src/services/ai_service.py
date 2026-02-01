import os
import json
import re
import uuid
from typing import Dict, Any
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from src.models.crisis_schema import CrisisAlert

# --- 1. CONFIGURATION: LOAD .ENV FILE ---
# Load .env from the project root
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_env_path = os.path.join(_project_root, ".env")
print(f"--- DEBUG: Looking for .env at: {_env_path} (exists: {os.path.exists(_env_path)}) ---")
load_dotenv(_env_path)

# DEBUG: Check terminal to confirm keys are loaded
print(f"--- DEBUG: API KEY LOADED: {os.getenv('IBM_WATSONX_API_KEY') is not None} ---")

class CrisisNodeAIEngine:
    def __init__(self):
        # 2. LOAD CREDENTIALS
        self.api_key = os.getenv("IBM_WATSONX_API_KEY")
        self.project_id = os.getenv("IBM_WATSONX_PROJECT_ID")
        self.url = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.credentials = {"url": self.url, "apikey": self.api_key}
        print(f"--- DEBUG: API_KEY present: {self.api_key is not None and len(self.api_key) > 0} ---")
        print(f"--- DEBUG: PROJECT_ID present: {self.project_id is not None and len(self.project_id) > 0} ---")

        # 3. INITIALIZE MODEL (With Error Handling)
        self.model = None
        if self.api_key and self.project_id:
            try:
                self.model = ModelInference(
                    model_id="ibm/granite-3-3-8b-instruct",
                    params={
                        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                        GenParams.MAX_NEW_TOKENS: 900,
                        GenParams.TEMPERATURE: 0.3,
                    },
                    credentials=self.credentials,
                    project_id=self.project_id
                )
                print("--- SUCCESS: Watsonx Model Connected and Ready ---")
            except Exception as e:
                print(f"--- ERROR: Model Connection Failed: {e} ---")
        else:
            print("--- ERROR: Missing API Key or Project ID in .env file ---")

    def _parse_json_response(self, text_output: str) -> Dict[str, Any]:
        """Ensures the AI output is valid data for the dashboard"""
        try:
            return json.loads(text_output)
        except json.JSONDecodeError:
            # Fallback regex to find JSON blocks if the model adds extra text
            match = re.search(r'\{.*\}', text_output, re.DOTALL)
            return json.loads(match.group()) if match else {"raw": text_output}

    def generate_plan(self, alert: CrisisAlert):
        # --- CRASH PREVENTION: Handle Missing Model ---
        if not self.model:
            return {
                "incident_id": "ERROR-NO-MODEL",
                "final_plan_markdown": "## SYSTEM ERROR\n\n*The AI Model failed to connect.\n\nPossible Causes:\n1. IBM_WATSONX_PROJECT_ID is missing in your .env file.\n2. The API Key is invalid.\n\n*Check the VS Code Terminal for detailed error logs.",
                "agent_details": {"status": "failed", "reason": "Model not initialized"}
            }

        alert_json = alert.model_dump_json()

        try:
            # Step 1: Automated Assessment Agent
            assessment_raw = self.model.generate_text(
                prompt=f"[INST] You are a UN Disaster Assessment Officer. Analyze this incident: {alert_json}. Provide a technical JSON summary of impact. [/INST]"
            )
            assessment = self._parse_json_response(assessment_raw)

            # Step 2: Strategy Synthesis Agent
            final_plan = self.model.generate_text(
                prompt=f"[INST] Based on this assessment: {json.dumps(assessment)}, generate a comprehensive UN Response Plan in Markdown. Include sections for Logistics, Medical Support, and Immediate Actions. [/INST]"
            )

            return {
                "incident_id": f"CN-{uuid.uuid4().hex[:8].upper()}",
                "final_plan_markdown": final_plan,
                "agent_details": {"assessment": assessment}
            }
        except Exception as e:
            # Catch any runtime errors so the server doesn't crash (500)
            print(f"--- RUNTIME ERROR DURING GENERATION: {e} ---")
            return {
                "incident_id": "ERROR-RUNTIME",
                "final_plan_markdown": f"## AI Generation Failed\n\nError: {str(e)}",
                "agent_details": {"error": str(e)}
            }

# Singleton instance
ai_engine = CrisisNodeAIEngine()
