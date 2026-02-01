from pydantic import BaseModel, Field
from typing import Optional, Dict
import time

class NewsEntry(BaseModel):
    event: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None 
    link: str
    is_read: bool = False
    published: Optional[str] = None
    
    type: str = "news"
    timestamp: float = Field(default_factory=time.time)

    location: Optional[Dict] = {
        "name": None,
        "lat": None,
        "lon": None
    }

    class Config:
        from_attributes = True