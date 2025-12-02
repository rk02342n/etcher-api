from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


# {
#     "version": 1,
#     "article_id": "uuid-or-ulid",
#     "title": "string",
#     "subtitle": "string",
#     "body": "string",
#     "author": {
#         "address": "0x1234...abcd",
#         "display_name": "string",
#         "profile_image_cid": "optional CID"
#     },
#     "timestamps": {
#         "created_at": 1731881238,
#         "published_at": 1731881238,
#         "updated_at": 1731881238
#     },
#     "media": {
#         "images": [
#             {
#                 "cid": "bafybeih...",
#                 "caption": "string",
#                 "alt_text": "string"
#             }
#         ],
#         "videos": [
#             {
#                 "cid": "bafkreid...",
#                 "caption": "string"
#             }
#         ]
#     },
#     "tags": ["politics", "international", "opinion"],
#     "canonical_url": "optional link to your platform’s web view",
#     "summary": "string",
#     "locale": "en-US",
#     "integrity": {
#         "content_sha256": "hex string of raw article body",
#         "signature": "user_signed_message_optional",
#         "editorial_notes": ""
#     },
#     "pinning": {
#         "pinned_by": "your_service_name",
#         "pinned_at": 1731881238
#     }
# }

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

    author = relationship("Author", back_populates="posts")


# class Post(Base):
#     __tablename__ = "posts"
#
#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     title: Mapped[str] = mapped_column(Text, nullable=False)
#     subtitle: Mapped[str | None] = mapped_column(Text)
#     content: Mapped[str] = mapped_column(Text, nullable=False)
#     published_at: Mapped = mapped_column(TIMESTAMP(timezone=True))
#     author_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("authors.id", ondelete="CASCADE"),
#         nullable=False
#     )
#
#     author: Mapped["Author"] = relationship(back_populates="articles")