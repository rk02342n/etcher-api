from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify
from typing import List

from app.core.database import get_db
from app.models.publication import Publication
from app.models.author import Author
from app.schemas.publication import PublicationCreate, PublicationResponse, PublicationUpdate

router = APIRouter()

@router.post("/", response_model=PublicationResponse, status_code=201)
async def create_publication(publication: PublicationCreate, db: AsyncSession = Depends(get_db)):
    # Verify author exists
    result = await db.execute(select(Author).where(Author.id == publication.author_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Author not found")
    
    slug = slugify(publication.name)
    db_publication = Publication(**publication.model_dump(), slug=slug)
    db.add(db_publication)
    await db.commit()
    await db.refresh(db_publication)
    return db_publication

@router.get("/", response_model=List[PublicationResponse])
async def list_publications(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{publication_id}", response_model=PublicationResponse)
async def get_publication(publication_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication).where(Publication.id == publication_id))
    publication = result.scalar_one_or_none()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

@router.get("/slug/{slug}", response_model=PublicationResponse)
async def get_publication_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication).where(Publication.slug == slug))
    publication = result.scalar_one_or_none()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

@router.patch("/{publication_id}", response_model=PublicationResponse)
async def update_publication(publication_id: int, publication_update: PublicationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication).where(Publication.id == publication_id))
    publication = result.scalar_one_or_none()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    for key, value in publication_update.model_dump(exclude_unset=True).items():
        setattr(publication, key, value)
    
    await db.commit()
    await db.refresh(publication)
    return publication

@router.delete("/{publication_id}", status_code=204)
async def delete_publication(publication_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication).where(Publication.id == publication_id))
    publication = result.scalar_one_or_none()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    await db.delete(publication)
    await db.commit()