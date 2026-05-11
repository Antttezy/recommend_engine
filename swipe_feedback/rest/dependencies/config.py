from fastapi import Request
from swipe_feedback.config import Settings


def get_config(request: Request) -> Settings:
    return request.app.state.config
