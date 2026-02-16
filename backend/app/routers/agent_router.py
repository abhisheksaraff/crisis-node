import json
from fastapi import APIRouter, HTTPException, Body
from typing import Any
from app.services.agent_service import AgentService
from app.db.news_db import mark_all_news_read
router = APIRouter(prefix="/agent", tags=["AI Agent Operations"])
service = AgentService()

# --- 1. DISCOVERY ENDPOINT ---
@router.get("/context")
async def get_agent_context():
    """n8n calls this to see where news is happening vs where alerts exist."""
    return service.get_agent_context()

# --- 2. TRIAGE ENDPOINT ---
@router.get("/triage/{location}")
async def get_location_triage(location: str):
    """Gathers all evidence for a specific city for the agent to analyze."""
    data = service.prepare_location_data(location)
    if not data["new_news"]:
        raise HTTPException(status_code=404, detail=f"No new news found for {location}")
    return data

# --- 3. EXECUTION: CREATE ---
@router.post("/process-new")
async def create_new_alert(alert_data: Any = Body(...)):
    """Endpoint for agent to create a brand-new verified alert."""
    try:
        clean_data = service.process_new_alert(alert_data)
        return {"status": "created", "result": clean_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 4. EXECUTION: UPDATE ---
@router.post("/process-update")
async def add_alert_source(alert_source: Any = Body(...)):
    """Endpoint for agent to add news to an existing alert."""
    try:
        alert_id = alert_source.get("alert_id")
        new_source = alert_source.get("new_source")
        
        if isinstance(new_source, str):
            try:
                new_source = json.loads(new_source)
            except json.JSONDecodeError:
                pass
        
        return service.add_alert_source(alert_id, new_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 5. MANAGEMENT ---
@router.post("/workflow-complete")
async def workflow_complete(payload: dict):
    if payload.get("status") == "success":
        print("n8n signaled success. Updating database...")
        mark_all_news_read() 
        return {"status": "Database updated"}
    
    return {"status": "No action taken"}

@router.post("/resolve")
async def resolve_incident(alert_id: str = Body(..., embed=True)):
    """Finalizes an incident (marks inactive)."""
    try:
        return service.resolve_alert(alert_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))