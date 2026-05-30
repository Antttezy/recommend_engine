from collections import deque
from uuid import UUID

from feed.core.models import CachedItem
from feed.core import ports


class FeedCacheClientMock(ports.FeedCacheClient):
    def __init__(self):
        self.storage: dict[UUID, deque[CachedItem]] = {}

    async def get_next_item(self, user_id: UUID):
        user_queue = self.storage.get(user_id)
        if not user_queue:
            return None

        return user_queue[0]

    async def pop_item(self, user_id: UUID):
        user_queue = self.storage.get(user_id)

        if not user_queue or len(user_queue) == 0:
            return None

        return user_queue.popleft()

    async def push_items(self, user_id: UUID, items: list[CachedItem]):
        if user_id not in self.storage:
            self.storage[user_id] = deque()

        self.storage[user_id].extend(items)
