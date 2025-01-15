from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from .config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.now(), nullable=False)
