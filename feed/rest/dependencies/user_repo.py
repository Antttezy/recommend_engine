from fastapi import Depends
from qdrant_client import AsyncQdrantClient

from infrastructure.vectorized_user_repo import QdrantUserRepo
from .qdrant_client import qdrant_client


def user_repo(qdrant: AsyncQdrantClient = Depends(qdrant_client)):
    return QdrantUserRepo(qdrant)
