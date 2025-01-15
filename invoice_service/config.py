import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/dbname")
KAFKA_SERVER: str = os.getenv("KAFKA_SERVER", "localhost:9092")
KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "new_applications")


engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    from .models import SQLModel

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
