from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify
from typing import List

from app.core.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter()

@router.post("/", response_model=AuthorResponse, status_code=201)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    result = db.execute(select(Author).where(Author.email == author.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #slug = slugify(author.name)
    #db_author = Author(**author.model_dump(), slug=slug)
    db_author = Author(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[AuthorResponse])
async def list_authors(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Author).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Author).where(Author.id == author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/slug/{slug}", response_model=AuthorResponse)
async def get_author_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.slug == slug))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.patch("/{author_id}", response_model=AuthorResponse)
async def update_author(author_id: int, author_update: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.id == author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author_update.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    
    await db.commit()
    await db.refresh(author)
    return author

@router.delete("/{author_id}", status_code=204)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.id == author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    await db.delete(author)
    await db.commit()