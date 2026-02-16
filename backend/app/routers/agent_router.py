import json
import httpx
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
    print("process-new", alert_data)
    try:
        #clean_data = alert_data.model_dump(mode='json') 
        clean_data = service.process_new_alert(alert_data)
        return {"status": "created", "result": clean_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 4. EXECUTION: UPDATE ---
@router.post("/process-update")
async def add_alert_source(alert_source: Any = Body(...)):
    """Endpoint for agent to add news to an existing alert."""
    print("process-update", alert_source)
    try:
        #return service.add_alert_source(alert_id, new_source.model_dump(mode='json'))
        # clean_data = service.add_alert_source(new_source)
        # return service.add_alert_source(alert_id, clean_data)
        alert_id = alert_source.get("alert_id")
        new_source = alert_source.get("new_source")

        # Use your service to clean the news data
        # clean_data = service.process_new_alert(new_source)
        
        if isinstance(new_source, str):
            try:
                new_source = json.loads(new_source)
            except json.JSONDecodeError:
                pass
        
        return service.add_alert_source(alert_id, new_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 5. MANAGEMENT ---
@router.post("/resolve")
async def resolve_incident(alert_id: str = Body(..., embed=True)):
    """Finalizes an incident (marks inactive)."""
    try:
        return service.resolve_alert(alert_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))