from typing import List, Dict, Any
from app.db.alerts_db import (
    read_alerts,
    add_custom_action,
    update_alert_action_status,
    mark_alert_done
)

class UserService:
    def list_active_incidents(self) -> List[Dict[str, Any]]:
        """Web router calls this to get the main dashboard feed."""
        return read_alerts(active_only=True)

    def add_user_defined_task(self, alert_id: str, task_text: str):
        """Web router calls this when user types a custom task in the UI."""
        return add_custom_action(alert_id, task_text)

    def set_task_completion(self, alert_id: str, task_index: int, is_done: bool):
        """Web router calls this when user clicks a checkbox on a task."""
        return update_alert_action_status(alert_id, task_index, is_done)

    def close_incident(self, alert_id: str):
        """Web router calls this for the manual 'Resolve' button."""
        return mark_alert_done(alert_id)