from fastapi import APIRouter
from app.api.endpoints import authors, publications, posts, subscribers

api_router = APIRouter()

api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(publications.router, prefix="/publications", tags=["publications"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(subscribers.router, prefix="/subscribers", tags=["subscribers"])