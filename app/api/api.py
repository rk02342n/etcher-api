from fastapi import APIRouter
from app.api.endpoints import authors, posts

api_router = APIRouter()

api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
