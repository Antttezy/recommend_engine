from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
    QDRANT_URL: str
    VECTOR_PROCESSOR_ENDPOINT: str
    KAFKA_LISTENER: str

    LOG_LEVEL: str = Field("INFO")


def load_config():
    return Settings()
