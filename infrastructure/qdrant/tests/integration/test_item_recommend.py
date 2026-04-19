import random
import uuid

import numpy
import pytest

from core.models import VectorizedItem, VectorizedUser, Gender, Embedding
from core.const import EMBEDDING_LENGTH

from infrastructure.qdrant.migration import QdrantMigrator
from infrastructure.vectorized_item_repo import QdrantItemRepo
from infrastructure.item_recommend import QdrantItemRecommend
from infrastructure.qdrant.const import ITEM_COLLECTION_NAME, USER_COLLECTION_NAME
from fixtures import skip_not_integration, qdrant_client, random_embedding


def random_normalized_embedding():
    data = [random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)]
    data = numpy.array(data)
    norm = numpy.linalg.norm(data)
    data = data / norm
    data = data.tolist()
    return Embedding(data)


@pytest.mark.asyncio
async def test_item_create(skip_not_integration, qdrant_client, random_embedding):
    items = [
        VectorizedItem(uuid.uuid4(), True, Gender.MALE, random_normalized_embedding()),
        VectorizedItem(uuid.uuid4(), False, Gender.MALE, random_normalized_embedding()),
        VectorizedItem(uuid.uuid4(), True, Gender.FEMALE, random_normalized_embedding()),
        VectorizedItem(uuid.uuid4(), False, Gender.FEMALE, random_normalized_embedding()),
        VectorizedItem(uuid.uuid4(), False, Gender.NOT_SPECIFIED, random_normalized_embedding()),
        VectorizedItem(uuid.uuid4(), True, Gender.NOT_SPECIFIED, random_normalized_embedding()),
    ]

    try:
        migrator = QdrantMigrator(qdrant_client)
        await migrator.create_collections_if_needed()
        item_repo = QdrantItemRepo(qdrant_client)
        item_recommend = QdrantItemRecommend(qdrant_client)

        try:
            for item in items:
                await item_repo.add(item)
        except:
            pytest.fail("failed to add items to repo")

        new_user_emb = Embedding(data=[0.0] * EMBEDDING_LENGTH)
        user = VectorizedUser(uuid.uuid4(), Gender.MALE, new_user_emb)

        recommended: list[VectorizedItem] = await item_recommend.get_recommended(user, 5)
        assert len(recommended) == 2

        for r in recommended:
            assert r.item_id in [items[0].item_id, items[5].item_id]
            src_item = next(filter(lambda a: a.item_id == r.item_id, items))
            assert src_item.in_stock == r.in_stock
            assert src_item.sex == r.sex

            assert r.in_stock
            assert r.sex in [Gender.MALE, Gender.NOT_SPECIFIED]

    finally:
        await qdrant_client.delete_collection(ITEM_COLLECTION_NAME)
        await qdrant_client.delete_collection(USER_COLLECTION_NAME)
        await qdrant_client.close()
