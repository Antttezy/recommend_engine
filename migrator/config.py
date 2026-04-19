from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_URL: str
    LOG_LEVEL: str = Field("INFO")
