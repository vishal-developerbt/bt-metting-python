from app.core.config import settings
import logging
from app.utils.email import send_email
# from app.routes.ws_notifications import manager
from app.websocket.connection_manager import manager
import asyncio
import json
from aiokafka import AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
logging.basicConfig(
    level=logging.INFO,  # Minimum level to show (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
# client = AsyncIOMotorClient(settings.MONGO_URL)
# notification_collection = client.notifications.notifications

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
notification_collection = db["notifications"]

consumer_task = None
consumer_instance = None

async def consume_notifications():
    global consumer_instance
    consumer_instance = AIOKafkaConsumer(
        # settings.KAFKA_TOPIC,
        settings.BOOKING_KAFKA_TOPIC, 
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="notification-service-group",
        auto_offset_reset="earliest"
    )
    await consumer_instance.start()
    print("Kafka consumer started")
    print("Mongo URL:", settings.MONGO_URL)
    print("Database:", settings.DATABASE_NAME)
    logger.info("Kafka consumer started")

    try:
        async for msg in consumer_instance:
            print("Kafka message received:", msg.value.decode()) 
            logger.debug(f"Kafka message received: {msg.value.decode()}")
            
            try:
                data = json.loads(msg.value.decode())
            except json.JSONDecodeError:
                logger.error("Invalid JSON received from Kafka")
                continue
            
            # BROADCAST TO WEBSOCKET CLIENTS
            if manager.active_connections:
                print("📡 Broadcasting to", len(manager.active_connections), "clients")

                await manager.broadcast({
                    "type": "new_booking",
                    "data": data
                })
            else:
                print("No WebSocket clients connected")
                logger.warning("No WebSocket clients connected")


            user_email = data.get("user_email")
            booking_id = data.get("booking_id")

            notification_data = {
            "user_id": data.get("user_id"),
            "email": data.get("user_email"),
            "message": f"Booking confirmed! ID: {booking_id}",
            "status": "pending",
            "timestamp": datetime.now(timezone.utc)
        }
            print(notification_data)
            logger.info(notification_data)
            # Save to MongoDB
            result = await notification_collection.insert_one(notification_data)
            print(f" Saved notification to MongoDB: {result.inserted_id}")

            # Send email
            try:
                print(f"✉️ Sending email to {user_email}")
                await send_email(
                    to=user_email,
                    subject="Booking Confirmation",
                    body=notification_data["message"]
                )
                # Update status to sent
                await notification_collection.update_one(
                    {"_id": result.inserted_id},
                    {"$set": {"status": "sent"}}
                )
                print(f"Notification sent to {user_email}")
            except Exception as e:
                print(f"Failed to send email to {user_email}: {e}")
                logger.error(f"Failed to send email to {user_email}: {e}")
                await notification_collection.update_one(
                    {"_id": result.inserted_id},
                    {"$set": {"status": "failed"}}
                )

    except asyncio.CancelledError:
        print(" Kafka consumer task cancelled")
    finally:
        await consumer_instance.stop()
        consumer_instance = None
        print(" Kafka consumer stopped")


async def start_notification_consumer():
    global consumer_task
    if consumer_task is None or consumer_task.done():
        consumer_task = asyncio.create_task(consume_notifications())
        print(" Kafka consumer task started")


async def stop_notification_consumer():
    global consumer_task, consumer_instance
    if consumer_task and not consumer_task.done():
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    if consumer_instance:
        await consumer_instance.stop()
        consumer_instance = None
    print(" Kafka consumer fully stopped")