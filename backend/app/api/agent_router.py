from fastapi import APIRouter
from backend.app.services.agent_service import agent_service

router = APIRouter()

@router.post("/{alert_id}")
def post_execute(alert_id: int):
    pass