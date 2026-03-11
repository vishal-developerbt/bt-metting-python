from pydantic import BaseModel
from datetime import datetime


class NotificationCreate(BaseModel):
    user_id: int
    email: str
    message: str


class NotificationResponse(NotificationCreate):
    status: str
    timestamp: datetime


    