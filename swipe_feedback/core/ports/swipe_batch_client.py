import abc
from uuid import UUID
from core import models


class SwipeBatchClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def push_feedback(self, user_id: UUID, feedback: models.ItemFeedback):
        ...

    @abc.abstractmethod
    async def get_feedback_count(self, user_id: UUID) -> int:
        ...

    @abc.abstractmethod
    async def get_feedback_items(self, user_id: UUID) -> list[models.ItemFeedback]:
        ...

    @abc.abstractmethod
    async def clear_feedback(self, user_id: UUID):
        ...
