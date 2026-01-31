# service layer
from fastapi import HTTPException

def get_all_alerts():
    return {"Crisis": "Node"}

def get_alert(alert_id: int, q: str = None):
    return {"alert_id": alert_id, "q": q}

def read_alert(alert_id: int, q: str = None):
    return {"alert_id": alert_id, "q": q}