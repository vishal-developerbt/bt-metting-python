# 7️⃣ booking-service/app/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
import asyncio

from app import models
from app import schemas
# from .database import get_db
from app.database import get_db
# from .core.config import settings
from app.core.config import settings
# from app.kafka.producer import send_message
from app.kafka.producer import send_message
router = APIRouter()
security = HTTPBearer()

# -----------------------
# JWT Auth
# -----------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------
# Test endpoint
# -----------------------
@router.get("/")
def test():
    return {"message": "Booking Service Running"}

# -----------------------
# Create booking
# -----------------------

# @router.post("/bookings")
# async def create_booking(
#     booking: schemas.BookingCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     # Check if room is already booked for the time slot
#     existing_booking = db.query(models.Booking).filter(
#         models.Booking.room_id == booking.room_id,
#         models.Booking.date == booking.date,
#         models.Booking.start_time < booking.end_time,
#         models.Booking.end_time > booking.start_time,
#     ).first()

#     if existing_booking:
#         raise HTTPException(
#             status_code=400,
#             detail="Room already booked for this time slot",
#         )

#     # Save booking in DB
#     new_booking = models.Booking(
#         user_id=int(current_user["sub"]),
#         **booking.model_dump()
#     )

#     db.add(new_booking)
#     db.commit()
#     db.refresh(new_booking)

#     # Send Kafka event asynchronously
#     event_data = {
#         "booking_id": new_booking.id,
#         "user_email": current_user.get("email"),
#         "room_id": new_booking.room_id,
#         "date": str(new_booking.date),
#         "start_time": str(new_booking.start_time),
#         "end_time": str(new_booking.end_time),
#         "timestamp": datetime.now(timezone.utc).isoformat(),
#     }
#     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#     # Create task in the async event loop
#     await asyncio.create_task(send_message(event_data))
#     print("#############################################")

#     return new_booking


# from fastapi import Request

# @router.post("/bookings")
# async def create_booking(
#     booking: schemas.BookingCreate,
#     request: Request,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     # Check if room is already booked for the time slot
#     existing_booking = db.query(models.Booking).filter(
#         models.Booking.room_id == booking.room_id,
#         models.Booking.date == booking.date,
#         models.Booking.start_time < booking.end_time,
#         models.Booking.end_time > booking.start_time,
#     ).first()

#     if existing_booking:
#         raise HTTPException(
#             status_code=400,
#             detail="Room already booked for this time slot",
#         )

#     # Save booking in DB
#     new_booking = models.Booking(
#         user_id=int(current_user["sub"]),
#         **booking.model_dump()
#     )

#     db.add(new_booking)
#     db.commit()
#     db.refresh(new_booking)

#     # Prepare event
#     event_data = {
#         "booking_id": new_booking.id,
#         "user_email": current_user.get("email"),
#         "room_id": new_booking.room_id,
#         "date": str(new_booking.date),
#         "start_time": str(new_booking.start_time),
#         "end_time": str(new_booking.end_time),
#         "timestamp": datetime.now(timezone.utc).isoformat(),
#     }

#     # ✅ Option 1 — Fire and forget (recommended)
#     asyncio.create_task(
#         send_message(
#             request.app,
#             settings.BOOKING_KAFKA_TOPIC,
#             event_data
#         )
#     )

#     return new_booking

from fastapi import Request, BackgroundTasks
from app.kafka.producer import send_message
from app.core.config import settings
from datetime import datetime, timezone

@router.post("/bookings")
async def create_booking(
    booking: schemas.BookingCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    # Save booking in DB (Postgres)
    new_booking = models.Booking(
        user_id=int(current_user["sub"]),
        **booking.model_dump()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Prepare Kafka message
    event_data = {
        "booking_id": new_booking.id,
        "user_id": current_user.get("id"),
        "user_email": current_user.get("email"),
        "room_id": new_booking.room_id,
        "date": str(new_booking.date),
        "start_time": str(new_booking.start_time),
        "end_time": str(new_booking.end_time),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Fire-and-forget via background task
    background_tasks.add_task(
        send_message,
        request.app,
        settings.BOOKING_KAFKA_TOPIC,
        event_data
    )

    return new_booking