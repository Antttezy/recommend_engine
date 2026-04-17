from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
    GRPC_PORT: int = Field(8001)
    GRPC_REFLECTION: bool = Field(False)
    LOG_LEVEL: str = Field("INFO")
    CLIP_MODEL: str
    CLIP_PROCESSOR: str

    FEEDBACK_LIKE_LEARNING_RATE: float
    FEEDBACK_DISLIKE_LEARNING_RATE: float
    FEEDBACK_DECAY: float


def load_config() -> Settings:
    return Settings()
