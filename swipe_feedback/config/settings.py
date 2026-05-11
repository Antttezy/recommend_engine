import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


OAUTH_TOKEN_URL = os.getenv('OAUTH_TOKEN_URL')
OAUTH_SCHEME = os.getenv('OAUTH_SCHEME', "Bearer")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
    QDRANT_URL: str
    VALKEY_URL: str
    VECTOR_PROCESSOR_ENDPOINT: str
    JWT_ALGORITHM: str
    JWT_KEY: str
    FEEDBACK_BATCH_ZERO: int
    FEEDBACK_BATCH_DEFAULT: int

    LOG_LEVEL: str = Field("INFO")
    HTTP_PORT: int = Field(8000)


def load_settings():
    return Settings()
