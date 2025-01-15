from aiokafka import AIOKafkaProducer
from .config import KAFKA_SERVER
import json

producer = None


async def init_kafka():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()


async def shutdown_kafka():
    global producer
    if producer:
        await producer.stop()
