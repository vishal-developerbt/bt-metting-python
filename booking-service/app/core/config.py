from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "defaultsecretkey")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:password@postgres:5432/meetingdb")
    KAFKA_BOOTSTRAP_SERVERS: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    BOOKING_KAFKA_TOPIC: str = os.environ.get("BOOKING_KAFKA_TOPIC", "booking-topic")

    class Config:
        env_file = "../../.env"

settings = Settings()