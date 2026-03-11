from aiokafka import AIOKafkaProducer
from app.core.config import settings  
import json
import logging


logger = logging.getLogger(__name__)

async def start_producer(app):
    print("🚀 Starting Kafka producer...")
    try:
        app.state.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await app.state.producer.start()
        print("✅ Kafka producer started successfully")
    except Exception as e:
        print("❌ Kafka failed to start:", e)
        app.state.producer = None

async def stop_producer(app):
    producer = getattr(app.state, "producer", None)
    if producer:
        await producer.stop()
        logger.info("🛑 Kafka producer stopped")


async def send_message(app, topic: str, data: dict):
    producer = getattr(app.state, "producer", None)

    if producer is None:
        logger.error("❌ Kafka producer is not initialized")
        return

    await producer.send_and_wait(topic, data)
    print(f"📤 Sent Kafka message to topic {topic}")