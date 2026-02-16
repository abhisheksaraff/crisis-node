from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uuid
from datetime import datetime, timezone

class AlertAction(BaseModel):
    task: str
    done: bool = False

class AlertSource(BaseModel):
    name: Optional[str] = None
    url: str
    timestamp: Optional[str] = None

class AlertEntry(BaseModel):
    alert_id: Optional[uuid.UUID] = None  # Supabase Generated
    event: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    
    actions: List[AlertAction] = []
    sources: List[AlertSource] = []
    
    location: Dict = {
        "name": None,
        "lat": None,
        "lon": None
    }
    
    is_read: bool = False
    is_active: bool = True

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True