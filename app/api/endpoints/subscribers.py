from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List

from app.core.database import get_db
from app.models.subscriber import Subscriber
from app.models.publication import Publication
from app.schemas.subscriber import SubscriberCreate, SubscriberResponse

router = APIRouter()

@router.post("/", response_model=SubscriberResponse, status_code=201)
async def subscribe(subscriber: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    # Verify publication exists
    pub_result = await db.execute(select(Publication).where(Publication.id == subscriber.publication_id))
    if not pub_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Publication not found")
    
    # Check if already subscribed
    result = await db.execute(
        select(Subscriber).where(
            and_(
                Subscriber.email == subscriber.email,
                Subscriber.publication_id == subscriber.publication_id
            )
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already subscribed")
    
    db_subscriber = Subscriber(**subscriber.model_dump())
    db.add(db_subscriber)
    await db.commit()
    await db.refresh(db_subscriber)
    return db_subscriber

@router.get("/publication/{publication_id}", response_model=List[SubscriberResponse])
async def list_subscribers(publication_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Subscriber)
        .where(Subscriber.publication_id == publication_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.delete("/{subscriber_id}", status_code=204)
async def unsubscribe(subscriber_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
    subscriber = result.scalar_one_or_none()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    await db.delete(subscriber)
    await db.commit()