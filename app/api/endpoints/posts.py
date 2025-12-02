from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from slugify import slugify
from datetime import datetime
from typing import List
import uuid

from app.core.database import get_db
from app.models.post import Post
from app.models.author import Author
from app.models.publication import Publication
from app.schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter()

@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    # Verify author and publication exist
    author_result = db.execute(select(Author).where(Author.id == post.author_id))
    if not author_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Author not found")
    
#     pub_result = db.execute(select(Publication).where(Publication.id == post.publication_id))
#     if not pub_result.scalar_one_or_none():
#         raise HTTPException(status_code=404, detail="Publication not found")
    
#     slug = slugify(post.title)
    published_at = datetime.utcnow() # if post.is_published else None
    
    db_post = Post(**post.model_dump(), published_at=published_at)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0, 
    limit: int = 20, 
#     published_only: bool = True,
#     publication_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Post)
    
#     if published_only:
#         query = query.where(Post.is_published == True)
    
#     if publication_id:
#         query = query.where(Post.publication_id == publication_id)
    
    query = query.order_by(Post.published_at.desc()).offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/byauthor/{author_id}", response_model=List[PostResponse])
async def list_posts(
    author_id: str,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    query = select(Post).where(Post.author_id == author_id)
    query = query.order_by(Post.published_at.desc()).offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()

@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_update.model_dump(exclude_unset=True)

    # Handle publishing logic
#     if 'is_published' in update_data and update_data['is_published'] and not post.is_published:
#         update_data['published_at'] = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(post, key, value)
    
    await db.commit()
    await db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await db.delete(post)
    await db.commit()
