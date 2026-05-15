from uuid import UUID

from valkey.asyncio import Valkey

from core.models import ItemFeedback

from .mapping import map_to_batched_feedback, map_from_batched_feedback
from .models import BatchedFeedback
from .const import get_swipe_batch_key


class SwipeBatchClient:
    def __init__(self, valkey_client: Valkey):
        self.__valkey_client = valkey_client

    async def push_feedback(self, user_id: UUID, feedback: ItemFeedback):
        mapped = map_to_batched_feedback(feedback)
        key = get_swipe_batch_key(user_id)
        formatted = mapped.model_dump_json(by_alias=True)
        await self.__valkey_client.lpush(key, formatted)

    async def get_feedback_count(self, user_id: UUID) -> int:
        key = get_swipe_batch_key(user_id)
        return await self.__valkey_client.llen(key)

    async def get_feedback_items(self, user_id: UUID) -> list[ItemFeedback]:
        key = get_swipe_batch_key(user_id)
        items = await self.__valkey_client.lrange(key, 0, -1)
        return [map_from_batched_feedback(BatchedFeedback.model_validate_json(x)) for x in items]

    async def clear_feedback(self, user_id: UUID):
        key = get_swipe_batch_key(user_id)
        await self.__valkey_client.delete(key)
