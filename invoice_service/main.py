from fastapi import FastAPI
from invoice_service.routes.invoice import router as invoice_routes


app = FastAPI()

app.include_router(router=invoice_routes, prefix="/applications", tags=["Applications"])


@app.on_event("startup")
async def startup_event():
    from .config import init_db

    await init_db()
