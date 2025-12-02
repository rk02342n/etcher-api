from pydantic import BaseModel, EmailStr
from datetime import datetime

class SubscriberCreate(BaseModel):
    email: EmailStr
    publication_id: int

class SubscriberResponse(BaseModel):
    id: int
    email: EmailStr
    publication_id: int
    subscribed_at: datetime
    
    class Config:
        from_attributes = True