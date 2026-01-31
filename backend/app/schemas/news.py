from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsEntry(BaseModel):
    event: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None 
    link: str
    published: Optional[str] = None
    
    class Config:
        from_attributes = True