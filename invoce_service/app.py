from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    from app.database import init_db
    from app.kafka import init_kafka

    await init_db()
    await init_kafka()


@app.on_event("shutdown")
async def shutdown_event():
    from app.kafka import shutdown_kafka

    await shutdown_kafka()
