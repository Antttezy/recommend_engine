from fastapi import Depends
from qdrant_client import AsyncQdrantClient

from infrastructure.item_recommend import QdrantItemRecommend
from .qdrant_client import qdrant_client


def item_recommend(qdrant: AsyncQdrantClient = Depends(qdrant_client)):
    return QdrantItemRecommend(qdrant)
