from fastapi import APIRouter
from backend.app.services.agent_service import agent_service

router = APIRouter()

@router.post("/{alert_id}")
def post_execute(alert_id: int):
    pass

@router.post("/process-batch", summary="Process next batch of raw news")
async def trigger_batch_processing():
    """
    Skill for Agent: Tells the backend to take the next 5 
    pending news items and run AI enrichment on them.
    """
    return await agent_service.process_pending_batch()