from fastapi import APIRouter, HTTPException, Query, Depends
from invoice_service.config import KAFKA_TOPIC, KAFKA_SERVER
from invoice_service.models import Application
from invoice_service.schemas import ApplicationCreate, ApplicationResponse
from invoice_service.config import get_db
import json
from aiokafka import AIOKafkaProducer
from sqlmodel import Session

router = APIRouter()


async def send_message(msg):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    try:
        metadata = await producer.send_and_wait(topic=KAFKA_TOPIC, value=msg)
        print(f"Message sent to {metadata.topic} partition {metadata.partition} at offset {metadata.offset}")
    finally:
        await producer.stop()


@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
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
    db: Session = Depends(get_db),
    user_name: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    query = db.query(Application)
    if user_name:
        query = query.filter(Application.user_name == user_name)
    total = await db.execute(query)
    return await db.execute(query.offset((page - 1) * size).limit(size))
