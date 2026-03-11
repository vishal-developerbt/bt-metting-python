# ==============================
# Standard Library Imports
# ==============================
from datetime import datetime, timezone

# ==============================
# Third-Party Imports
# ==============================
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import and_
from jose import jwt, JWTError

# ==============================
# Local Application Imports
# ==============================
from app import models, schemas
from app.database import get_db
from app.kafka.producer import send_message
from app.core.config import settings


# ==============================
# Router & Security
# ==============================
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
# List bookings for current user
# -----------------------
@router.get("/bookings", response_model=list[schemas.BookingResponse])
def list_bookings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Returns all bookings for the logged-in user.
    """
    user_id = int(current_user["sub"])
    bookings = db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")

    return bookings
# -----------------------

# Create booking
# -----------------------

@router.post("/bookings")
async def create_booking(
    booking: schemas.BookingCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Save booking in DB (Postgres)

    existing_booking = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.date == booking.date,
        models.Booking.status == "confirmed",
        and_(
            booking.start_time < models.Booking.end_time,
            booking.end_time > models.Booking.start_time
        )
    ).first()

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail=f"Room already booked until {existing_booking.end_time}"
        )

    # Save booking if no conflict
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
        "user_id": int(current_user["sub"]),
        "user_email": current_user.get("email"),
        "room_id": new_booking.room_id,
        "date": str(new_booking.date),
        "start_time": str(new_booking.start_time),
        "end_time": str(new_booking.end_time),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    
    background_tasks.add_task(
        send_message,
        request.app,
        settings.BOOKING_KAFKA_TOPIC,
        event_data
    )

    return new_booking

