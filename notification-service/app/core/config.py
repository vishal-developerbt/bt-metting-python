from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    BOOKING_KAFKA_TOPIC: str = "booking-topic"

    # MongoDB
    MONGO_URL: str = "mongodb://mongo:27017"
    DATABASE_NAME: str = "meeting_notifications"

    # Email
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",   # optional for local development
        extra="ignore"
    )


settings = Settings()