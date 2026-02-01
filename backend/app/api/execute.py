from fastapi import APIRouter
from backend.app.services.execute_service import execute_alert

router = APIRouter()

@router.post("/{alert_id}")
def post_execute(alert_id: int):
    return execute_alert(alert_id)