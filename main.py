from fastapi import FastAPI, HTTPException
from src.models.crisis_schema import CrisisAlert
from src.services.ibm_watson_service import ai_engine

app = FastAPI()

@app.post("/api/crisis/plan")
async def generate_crisis_plan(alert: CrisisAlert):
    try:
        # Call the logic from the service file
        result = ai_engine.generate_plan(alert)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))