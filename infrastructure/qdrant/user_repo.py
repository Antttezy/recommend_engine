import uuid

from qdrant_client import AsyncQdrantClient

from core import models, ports
from .const import ITEM_COLLECTION_NAME


class QdrantUserRepo(ports.VectorizedUserRepo):
    def __init__(self, client: AsyncQdrantClient):
        super().__init__()
        self.__client = client

    async def get_by_id(self, userid):
        users = await self.__client.retrieve(ITEM_COLLECTION_NAME, ids=[userid])
        if len(users) == 0:
            return

        user = users[0]
        user_id = uuid.UUID(user.payload['user_id'])
        sex = models.Gender(user.payload['sex'])
        embedding = models.Embedding(data=[x for x in user.vector])

        return models.VectorizedUser(
            item_id=user_id,
            sex=sex,
            embedding=embedding
        )

    async def add(self, vectorized_user):
        await self.upsert(vectorized_user)

    async def update(self, vectorized_user):
        await self.upsert(vectorized_user)

    async def upsert(self, vectorized_user: models.VectorizedUser):
        payload = {
            "user_id": str(vectorized_user.user_id),
            "sex": vectorized_user.sex.value
        }

        await self.__client.upsert(
            collection_name=ITEM_COLLECTION_NAME,
            points=[{
                "id": vectorized_user.user_id,
                "vector": vectorized_user.embedding.data,
                "payload": payload
            }]
        )
