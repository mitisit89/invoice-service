from fastapi import APIRouter, HTTPException, Query, Depends
from app.database import get_db
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka import AIOKafkaProducer
from invoice_service.kafka import producer, KAFKA_TOPIC

router = APIRouter()


@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    new_application = Application(user_name=application.user_name, description=application.description)
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    await producer.send_and_wait(
        KAFKA_TOPIC,
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
    user_name: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    query = db.query(Application)
    if user_name:
        query = query.filter(Application.user_name == user_name)
    total = await db.execute(query)
    return await db.execute(query.offset((page - 1) * size).limit(size))
