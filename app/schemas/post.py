from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class PostBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    content: str
    cover_image_url: Optional[str] = None
    content_cid: Optional[str] = None

class PostCreate(PostBase):
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    cover_image_url: Optional[str] = None
    content_cid: Optional[str] = None
    last_verified: Optional[datetime] = None
    address: Optional[str] = None

class PostResponse(PostBase):
    id: uuid.UUID
    published_at: Optional[datetime]
    last_verified: Optional[datetime]
    address: Optional[str]
    author_id: int

    class Config:
        from_attributes = True
