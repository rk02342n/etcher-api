from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    # bio: Optional[str] = None
    # avatar_url: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    name: str
    email: EmailStr
    # slug: str
    # created_at: datetime
    
    class Config:
        from_attributes = True