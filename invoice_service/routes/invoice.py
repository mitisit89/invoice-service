import json
from typing import Any
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import select

from invoice_service.config import KAFKA_SERVER, KAFKA_TOPIC
from invoice_service.config import get_db
from invoice_service.models import Application
from invoice_service.schemas import ApplicationCreate, ApplicationResponse
from invoice_service.logger import logging as logger

router = APIRouter()


async def send_message(msg: dict[str, Any]) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    try:
        logger.info(f"Sending message to Kafka: {msg}")
        metadata = await producer.send_and_wait(topic=KAFKA_TOPIC, value=msg)
        logger.info(f"Message sent to {metadata.topic} partition {metadata.partition} at offset {metadata.offset}")
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")
    finally:
        await producer.stop()


@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    new_application = Application(user_name=application.user_name, description=application.description)
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    await send_message(
        {
            "id": new_application.id,
            "user_name": new_application.user_name,
            "description": new_application.description,
            "created_at": new_application.created_at.isoformat(),
        },
    )

    return new_application


@router.get("/", response_model=list[ApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(get_db),
    user_name: str = Query(str, title="User Name", min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    page = await db.execute(select(Application).where(Application.user_name == user_name))
    return page.scalars().all()
