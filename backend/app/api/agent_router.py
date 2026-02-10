from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from backend.app.schemas.alerts import AlertEntry, AlertSource
from backend.app.services.agent_service import AgentService

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
async def create_new_alert(news_id: str, alert_data: AlertEntry):
    """Endpoint for agent to create a brand-new verified alert."""
    try:
        # Pass alert_data as a validated Pydantic model
        return service.process_new_alert(news_id, alert_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 4. EXECUTION: UPDATE ---
@router.post("/process-update")
async def update_alert_incident(alert_id: str, news_id: str, source_data: AlertSource):
    """Endpoint for agent to add news to an existing alert."""
    try:
        return service.update_existing_incident(alert_id, news_id, source_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 5. MANAGEMENT ---
@router.patch("/action-status")
async def update_task(alert_id: str, task_index: int, is_done: bool):
    """Allows agent to check off tasks in the alert actions list."""
    return service.sync_action_status(alert_id, task_index, is_done)

@router.post("/resolve/{alert_id}")
async def resolve_incident(alert_id: str):
    """Finalizes an incident (marks inactive)."""
    return service.resolve_alert(alert_id)