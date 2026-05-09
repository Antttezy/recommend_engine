from fastapi import Request
from feed.config import Settings


def get_config(request: Request) -> Settings:
    return request.app.state.config
