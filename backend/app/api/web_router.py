from fastapi import APIRouter
from backend.app.services.web_service import *

router = APIRouter()

@router.get("/")
def read_alerts():
    return get_all_alerts()

@router.get("/{alert_id}")
def read_alert(alert_id: int):
    return get_alert(alert_id)
