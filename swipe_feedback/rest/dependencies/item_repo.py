from fastapi import Depends
from qdrant_client import AsyncQdrantClient

from infrastructure.vectorized_item_repo import QdrantItemRepo
from .qdrant_client import qdrant_client


def item_repo(qdrant: AsyncQdrantClient = Depends(qdrant_client)):
    return QdrantItemRepo(qdrant)
