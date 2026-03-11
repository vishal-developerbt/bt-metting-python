from fastapi import APIRouter, WebSocket
from datetime import datetime, timezone
from app.models import NotificationCreate
from app.database import notification_collection
from app.utils.email import send_email
from app.websocket.connection_manager import manager

router = APIRouter()


@router.post("/notifications")
async def create_notification(notification: NotificationCreate):
    notification_data = notification.model_dump()

    notification_data["status"] = "sent"
    notification_data["timestamp"] = datetime.now(timezone.utc)

    # notification_collection.insert_one(notification_data)
    await notification_collection.insert_one(notification_data)

    return {"message": "Notification stored successfully"}



@router.get("/test-email")
async def test_email():
    await send_email(
        to="vishal@gmail.com", 
        subject="Test Email", 
        body="This is a test email."
    )
    return {"message": "Test email sent"}

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
        manager.disconnect(websocket)