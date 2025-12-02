# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import declarative_base
# from app.core.config import settings

# engine = create_async_engine(settings.DATABASE_URL, echo=True)
# async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()

# async def get_db():
#     async with async_session_maker() as session:
#         yield session

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Bright#1270@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = 'postgresql://rohitsaigopal:mypassword@localhost:5432/etcher_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()