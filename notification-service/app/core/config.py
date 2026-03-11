from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    BOOKING_KAFKA_TOPIC: str = os.environ.get("BOOKING_KAFKA_TOPIC", "booking-topic")   # <- must match Booking Service topic

    # MongoDB
    MONGO_URL: str = os.environ.get("MONGO_URL", "mongodb://mongo:27017")

    # Email
    EMAIL_HOST: str = os.environ.get("EMAIL_HOST", "")
    EMAIL_PORT: int = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_TLS: bool = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    EMAIL_HOST_USER: str = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD: str = os.environ.get("EMAIL_HOST_PASSWORD", "")

    model_config = SettingsConfigDict(
        env_file="/var/www/html/bt-metting-room/.env",  # <- absolute path
        extra="ignore"
    )

settings = Settings()