import pytest

from infrastructure.qdrant.migration import QdrantMigrator
from infrastructure.qdrant.const import ITEM_COLLECTION_NAME, USER_COLLECTION_NAME
from fixtures import skip_not_integration, qdrant_client


@pytest.mark.asyncio
async def test_migration(skip_not_integration, qdrant_client):
    try:
        migrator = QdrantMigrator(qdrant_client)
        await migrator.create_collections_if_needed()

        try:
            await qdrant_client.get_collection(ITEM_COLLECTION_NAME)
            await qdrant_client.get_collection(USER_COLLECTION_NAME)
        except:
            pytest.fail("collections not created")

    finally:
        await qdrant_client.delete_collection(ITEM_COLLECTION_NAME)
        await qdrant_client.delete_collection(USER_COLLECTION_NAME)
        await qdrant_client.close()
