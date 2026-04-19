import uuid

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny, ScoredPoint

from core import models, ports
from .const import ITEM_COLLECTION_NAME


class QdrantItemRecommend(ports.ItemRecommend):
    def __init__(self, client: AsyncQdrantClient):
        super().__init__()
        self.__client = client

    async def get_recommended(self, user, limit):
        in_stock = FieldCondition(
            key="in_stock",
            match=MatchValue(value=True)
        )

        genders = [models.Gender.NOT_SPECIFIED.value]

        if user.sex != models.Gender.NOT_SPECIFIED:
            genders.append(user.sex.value)

        query_filter = Filter(
            must=[
                in_stock,
                FieldCondition(key='sex', match=MatchAny(any=genders))
            ]
        )

        response = await self.__client.query_points(
            collection_name=ITEM_COLLECTION_NAME,
            query=user.embedding.data,
            query_filter=query_filter,
            limit=limit,
            with_vectors=True
        )

        return list(map(self.__map_scored_point, response.points))

    @staticmethod
    def __map_scored_point(item: ScoredPoint) -> models.VectorizedItem:
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
