from fastapi import Request
from qdrant_client import AsyncQdrantClient


def qdrant_client(request: Request) -> AsyncQdrantClient:
    return request.app.state.qdrant
