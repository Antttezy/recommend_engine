import json
from typing import Optional
from uuid import UUID

from valkey.asyncio import Valkey

from .models import CachedItem
from .const import get_items_list_key


class FeedCacheClient:
    def __init__(self, valkey_client: Valkey):
        self.__valkey_client = valkey_client

    async def push_items(self, user_id: UUID, items: list[CachedItem]):
        key = get_items_list_key(user_id)
        # Should probably acquire lock and check if list is empty

        values = [f'{{"item_id":"{item.item_id}"}}' for item in items]
        await self.__valkey_client.rpush(key, *values)

    async def get_next_item(self, user_id: UUID) -> Optional[CachedItem]:
        key = get_items_list_key(user_id)
        item = await self.__valkey_client.lindex(key, 0)

        if item is None:
            return

        return self.__json_to_item(item)

    async def pop_item(self, user_id: UUID):
        key = get_items_list_key(user_id)
        item = await self.__valkey_client.lpop(key)

        if item is None:
            return

        return self.__json_to_item(item)

    def __json_to_item(self, value):
        try:
            loaded = json.loads(value)
            item_id = loaded['item_id']
            item_id = UUID(item_id)
            return _CachedItemWrapper(item_id)
        except (ValueError, json.decoder.JSONDecodeError, KeyError) as e:
            raise Exception("Unexpected cache response") from e


class _CachedItemWrapper(CachedItem):
    def __init__(self, item_id: UUID):
        super().__init__()
        self.__item_id = item_id

    @property
    def item_id(self):
        return self.__item_id
