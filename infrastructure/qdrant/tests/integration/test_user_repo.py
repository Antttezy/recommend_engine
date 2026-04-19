import uuid

import pytest

from core.models import VectorizedUser, Gender

from infrastructure.qdrant.migration import QdrantMigrator
from infrastructure.vectorized_user_repo import QdrantUserRepo
from infrastructure.qdrant.const import ITEM_COLLECTION_NAME, USER_COLLECTION_NAME
from fixtures import skip_not_integration, qdrant_client, random_embedding


@pytest.mark.asyncio
async def test_user_create(skip_not_integration, qdrant_client, random_embedding):
    try:
        migrator = QdrantMigrator(qdrant_client)
        await migrator.create_collections_if_needed()
        user_repo = QdrantUserRepo(qdrant_client)

        user_id = uuid.uuid4()
        user = VectorizedUser(user_id, Gender.MALE, embedding=random_embedding)

        try:
            await user_repo.add(user)
        except:
            pytest.fail("failed to add user to repo")

        try:
            ret = await user_repo.get_by_id(user_id)
        except:
            pytest.fail("failed to get user by id")

        assert ret is not None
        assert ret.user_id == user_id
        assert ret.sex == Gender.MALE

        assert len(ret.embedding.data) == len(random_embedding.data)
        assert all([x == pytest.approx(y)
                    for x, y in zip(ret.embedding.data, random_embedding.data)])

    finally:
        await qdrant_client.delete_collection(ITEM_COLLECTION_NAME)
        await qdrant_client.delete_collection(USER_COLLECTION_NAME)
        await qdrant_client.close()
