from aiokafka import AIOKafkaProducer
from app.core.config import settings
import json
import logging
import asyncio
logger = logging.getLogger(__name__)

async def start_producer(app):
    logger.info(" Starting Kafka producer...")

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    retries = 10
    delay = 5  # seconds

    for attempt in range(retries):
        try:
            await producer.start()
            app.state.producer = producer
            logger.info(" Kafka producer started successfully")
            return
        except Exception as e:
            logger.warning(
                f"Kafka not ready (attempt {attempt + 1}/{retries}) — retrying in {delay}s..."
            )
            await asyncio.sleep(delay)

    logger.error(" Kafka connection failed after multiple retries")
    app.state.producer = None


async def stop_producer(app):
    producer = getattr(app.state, "producer", None)

    if producer:
        await producer.stop()
        logger.info(" Kafka producer stopped")


async def send_message(app, topic: str, data: dict):
    producer = getattr(app.state, "producer", None)

    if not producer:
        logger.error(" Kafka producer is not initialized")
        return

    try:
        await producer.send_and_wait(topic, data)
        logger.info(f" Sent Kafka message to topic '{topic}'")
    except Exception as e:
        logger.error(f" Failed to send Kafka message: {e}")