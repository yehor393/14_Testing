from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aioredis

REDIS_URL = "redis://localhost:6379"
DATABASE_URL = "sqlite:///./demo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def create_redis_pool():
    pool = await aioredis.create_redis_pool(REDIS_URL)
    return pool

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
