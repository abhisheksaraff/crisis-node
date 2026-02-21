from fastapi import APIRouter
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User Actions"])
user_service = UserService()

@router.get("/alerts")
async def get_alerts():
    return user_service.list_active_incidents()

@router.post("/alerts/{alert_id}/actions/custom")
async def post_custom_task(alert_id: str, task_name: str):
    """Adds a human-inputted task to the alert's action list."""
    return user_service.add_user_defined_task(alert_id, task_name)

@router.patch("/alerts/{alert_id}/actions/{index}")
async def patch_task_status(alert_id: str, index: int, done: bool):
    """Updates whether a specific task (agent or user created) is finished."""
    return user_service.set_task_completion(alert_id, index, done)

@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    return user_service.close_incident(alert_id)