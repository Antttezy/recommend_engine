import uuid

import numpy
import pytest

from core.models import VectorizedItem, Gender

from infrastructure.qdrant.migration import QdrantMigrator
from infrastructure.vectorized_item_repo import QdrantItemRepo
from infrastructure.qdrant.const import ITEM_COLLECTION_NAME, USER_COLLECTION_NAME
from fixtures import skip_not_integration, qdrant_client, random_embedding


@pytest.mark.asyncio
async def test_item_create(skip_not_integration, qdrant_client, random_embedding):
    try:
        migrator = QdrantMigrator(qdrant_client)
        await migrator.create_collections_if_needed()
        item_repo = QdrantItemRepo(qdrant_client)

        item_id = uuid.uuid4()

        # Normalize item embedding
        arr = numpy.array(random_embedding.data)
        norm = numpy.linalg.norm(arr)
        arr = arr / norm
        random_embedding.data = arr.tolist()

        item = VectorizedItem(item_id, True, Gender.FEMALE, random_embedding)

        try:
            await item_repo.add(item)
        except:
            pytest.fail("failed to add item to repo")

        try:
            ret = await item_repo.get_by_id(item_id)
        except:
            pytest.fail("failed to get item by id")

        assert ret is not None
        assert ret.item_id == item_id
        assert ret.sex == Gender.FEMALE
        assert ret.in_stock == True

        assert len(ret.embedding.data) == len(random_embedding.data)
        assert all([x == pytest.approx(y)
                    for x, y in zip(ret.embedding.data, random_embedding.data)])

    finally:
        await qdrant_client.delete_collection(ITEM_COLLECTION_NAME)
        await qdrant_client.delete_collection(USER_COLLECTION_NAME)
        await qdrant_client.close()
