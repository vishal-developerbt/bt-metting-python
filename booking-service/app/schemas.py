from pydantic import BaseModel
from datetime import date, time


class BookingCreate(BaseModel):
    room_id: int
    date: date
    start_time: time
    end_time: time


class BookingResponse(BookingCreate):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True