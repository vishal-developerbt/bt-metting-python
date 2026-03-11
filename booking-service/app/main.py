from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from app.database import engine
from app import models
from app.routes.booking import router as booking_router
from app.routes.ws_notifications import router as ws_router
from app.kafka.producer import start_producer, stop_producer


# ---------------------------
# Create DB Tables
# ---------------------------
models.Base.metadata.create_all(bind=engine)


# ---------------------------
# Kafka Lifespan Manager
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 LIFESPAN IS RUNNING")

    # Start Kafka Producer
    #await start_producer(app)
    asyncio.create_task(start_producer(app))

    yield

    # Stop Kafka Producer
    await stop_producer(app)


# ---------------------------
# FastAPI App
# ---------------------------
app = FastAPI(
    title="Booking Service",
    lifespan=lifespan,
    root_path="/bookings"

)


# ---------------------------
# Include Routers
# ---------------------------
app.include_router(
    booking_router,
    prefix="/booking",
    tags=["Booking"]
)

app.include_router(
    ws_router,
    tags=["WebSocket"]
)