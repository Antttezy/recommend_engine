import abc
from typing import Optional
from uuid import UUID

from feed.core.models import CachedItem


class FeedCacheClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_next_item(self, user_id: UUID) -> Optional[CachedItem]:
        ...

    @abc.abstractmethod
    async def pop_item(self, user_id: UUID) -> Optional[CachedItem]:
        ...

    @abc.abstractmethod
    async def push_items(self, user_id: UUID, items: list[CachedItem]):
        ...
