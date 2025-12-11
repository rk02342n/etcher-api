from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    cover_image_url = Column(String(500), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    content_cid = Column(String(500), nullable=True)
    last_verified = Column(DateTime(timezone=True), nullable=True)
    address = Column(String(42), nullable=True)

    author = relationship("Author", back_populates="posts")
