from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=False)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
    publication = relationship("Publication", back_populates="subscribers")
    
    __table_args__ = (UniqueConstraint('email', 'publication_id', name='_email_publication_uc'),)
