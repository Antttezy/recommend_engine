from collections import deque
from uuid import UUID

from core.models import ItemFeedback
from swipe_feedback.core import ports


class SwipeBatchClientMock(ports.SwipeBatchClient):
    def __init__(self):
        self.storage: dict[UUID, deque[ItemFeedback]] = {}

    async def push_feedback(self, user_id, feedback):
        if user_id not in self.storage:
            self.storage[user_id] = deque()

        self.storage[user_id].appendleft(feedback)

    async def get_feedback_count(self, user_id):
        return len(self.storage.get(user_id, []))

    async def get_feedback_items(self, user_id):
        items = self.storage.get(user_id)

        if not items:
            return []

        return list(iter(items))

    async def clear_feedback(self, user_id):
        items = self.storage.get(user_id)

        if not items:
            return

        items.clear()
