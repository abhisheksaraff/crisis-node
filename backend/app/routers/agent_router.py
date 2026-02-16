import json
from fastapi import APIRouter, HTTPException, BackgroundTasks, Body
from typing import List, Dict, Any
from app.schemas.alerts import AlertEntry, AlertSource
from app.services.agent_service import AgentService

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

# from fastapi import APIRouter, HTTPException

# @router.get("/triage")
# async def get_location_triage(location: str):
#     """Gathers all evidence for a specific city for the agent to analyze."""
#     data = service.prepare_location_data(location)
#     if not data["new_news"]:
#         raise HTTPException(status_code=404, detail=f"No new news found for {location}")
#     return data

# --- 3. EXECUTION: CREATE ---
# @router.post("/process-new")
# async def create_new_alert(news_id: str, alert_data: AlertEntry):
#     """Endpoint for agent to create a brand-new verified alert."""
#     try:
#         # Pass alert_data as a validated Pydantic model
#         return service.process_new_alert(news_id, alert_data.model_dump())
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/process-new")
# async def create_new_alert(alert_data: Any = Body(...)):
#     """Endpoint for agent to create a brand-new verified alert."""
#     try:
#         print(object)
        
#         # Pass alert_data as a validated Pydantic model
#         clean_data = alert_data.model_dump(mode='json', exclude_unset=True)
#         return service.process_new_alert(clean_data)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=400, detail=str(e))

@router.post("/process-new")
async def create_new_alert(alert_data: Any = Body(...)):
    """Endpoint for agent to create a brand-new verified alert."""
    print(alert_data)
    print(type(alert_data))
    clean_data=json.dumps(alert_data)
    print(clean_data)
    print(type(clean_data))
    try:
        #clean_data = alert_data.model_dump(mode='json') 
        result = service.process_new_alert(alert_data)
        return {"status": "created", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 4. EXECUTION: UPDATE ---
@router.post("/process-update")
async def add_alert_source(alert_id: str, new_source: AlertSource):
    """Endpoint for agent to add news to an existing alert."""
    try:
        return service.add_alert_source(alert_id, new_source.model_dump(mode='json'))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 5. MANAGEMENT ---
@router.post("/resolve")
async def resolve_incident(alert_id: str):
    """Finalizes an incident (marks inactive)."""
    return service.resolve_alert(alert_id)