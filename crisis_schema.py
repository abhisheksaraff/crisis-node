from pydantic import BaseModel

class CrisisAlert(BaseModel):
    location: str
    severity: str  # LOW | MEDIUM | HIGH | CRITICAL
    event_type: str
    details: str