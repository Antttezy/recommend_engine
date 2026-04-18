import uuid

from qdrant_client import AsyncQdrantClient

from core import models, ports
from .const import ITEM_COLLECTION_NAME


class QdrantItemRepo(ports.VectorizedItemRepo):
    def __init__(self, client: AsyncQdrantClient):
        super().__init__()
        self.__client = client

    async def get_by_id(self, itemid):
        items = await self.__client.retrieve(ITEM_COLLECTION_NAME, ids=[itemid])
        if len(items) == 0:
            return

        item = items[0]
        item_id = uuid.UUID(item.payload['item_id'])
        in_stock = item.payload['in_stock']
        sex = models.Gender(item.payload['sex'])
        embedding = models.Embedding(data=[x for x in item.vector])

        return models.VectorizedItem(
            item_id=item_id,
            in_stock=in_stock,
            sex=sex,
            embedding=embedding
        )

    async def add(self, vectorized_item):
        await self.upsert(vectorized_item)

    async def update(self, vectorized_item):
        await self.upsert(vectorized_item)

    async def upsert(self, vectorized_item: models.VectorizedItem):
        payload = {
            "item_id": str(vectorized_item.item_id),
            "in_stock": vectorized_item.in_stock,
            "sex": vectorized_item.sex.value
        }

        await self.__client.upsert(
            collection_name=ITEM_COLLECTION_NAME,
            points=[{
                "id": vectorized_item.item_id,
                "vector": vectorized_item.embedding.data,
                "payload": payload
            }]
        )
