from fastapi import FastAPI
from invoice_service.routes.invoice import router as invoice_routes
from  contextlib import  asynccontextmanager

@asynccontextmanager
async  def lifespan(app:FastAPI)->None:
    from .config import init_db
    from .kafka import init_kafka,shutdown_kafka

    await init_db()
    await init_kafka()
    yield
    await shutdown_kafka()


app = FastAPI(lifespan=lifespan)

app.include_router(router=invoice_routes, prefix="/applications", tags=["Applications"])
