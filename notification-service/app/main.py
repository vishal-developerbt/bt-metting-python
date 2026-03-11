from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.routes import router
from app.kafka.consumer import start_notification_consumer, stop_notification_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_notification_consumer()
    yield
    await stop_notification_consumer()


app = FastAPI(title="Notification Service", lifespan=lifespan)

app.include_router(router)