from dataclasses import dataclass
import os
from uuid import UUID, uuid4

import pytest
from valkey.asyncio import Valkey

from infrastructure.feed_cache_client import FeedCacheClient
from infrastructure.feed_cache_client.const import get_items_list_key


@dataclass
class MockItem:
    item_id: UUID


@pytest.fixture
def valkey_client():
    host = os.getenv("VALKEY_HOST")
    port = os.getenv("VALKEY_PORT")
    return Valkey(host=host, port=int(port))


@pytest.fixture
def skip_not_integration():
    run_integration = os.getenv("RUN_INTEGRATION", None)

    if not run_integration:
        pytest.skip("--run-integration not set")


@pytest.fixture
def cleanup_client(valkey_client):
    async def cleanup(user_id: UUID):
        await valkey_client.delete(get_items_list_key(user_id))

    return cleanup


def test_key_formatting():
    user_id = UUID('12345678-1234-5678-1234-567812345678')
    key = get_items_list_key(user_id)

    assert key == 'user/12345678-1234-5678-1234-567812345678/feed'


@pytest.mark.asyncio
async def test_push_items(skip_not_integration, valkey_client, cleanup_client):
    try:
        cache = FeedCacheClient(valkey_client)
        user_id = uuid4()
        items = [MockItem(uuid4()) for _ in range(14)]

        await cache.push_items(user_id, items)

        retrieved = []

        while True:
            item = await cache.get_next_item(user_id)

            if item is None:
                break

            retrieved.append(item)

        assert len(items) == len(retrieved)
        assert all([a.item_id == b.item_id for a, b in zip(items, retrieved)])

    finally:
        await cleanup_client(user_id)
