from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PublicationBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

class PublicationCreate(PublicationBase):
    author_id: int

class PublicationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None

class PublicationResponse(PublicationBase):
    id: int
    slug: str
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True