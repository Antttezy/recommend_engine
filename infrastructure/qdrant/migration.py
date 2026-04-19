from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, HnswConfigDiff

from core.const import EMBEDDING_LENGTH
from .const import ITEM_COLLECTION_NAME, USER_COLLECTION_NAME


class QdrantMigrator:
    def __init__(self, client: AsyncQdrantClient):
        self.__client = client

    async def create_collections_if_needed(self):
        if not await self.__client.collection_exists(ITEM_COLLECTION_NAME):
            await self.__create_item_collection()

        if not await self.__client.collection_exists(USER_COLLECTION_NAME):
            await self.__create_user_collection()

    async def __create_item_collection(self):
        await self.__client.create_collection(
            ITEM_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_LENGTH,
                distance=Distance.COSINE,
            ),
            hnsw_config=HnswConfigDiff(m=32, ef_construct=200, full_scan_threshold=10000)
        )

        await self.__client.create_payload_index(
            collection_name=ITEM_COLLECTION_NAME,
            field_name="in_stock",
            field_schema="bool"
        )

        await self.__client.create_payload_index(
            collection_name=ITEM_COLLECTION_NAME,
            field_name="sex",
            field_schema="integer"
        )

    async def __create_user_collection(self):
        await self.__client.create_collection(
            USER_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_LENGTH,
                distance=Distance.DOT
            ),
            hnsw_config=HnswConfigDiff(m=0)  # We only get users by their ids, so disable HNSW
        )
