from dataclasses import dataclass
from uuid import UUID

from core import models, ports, errors
from swipe_feedback.core.ports import SwipeBatchClient


@dataclass
class BatchSize:
    zero: int
    default: int


class FeedbackUsecase:
    def __init__(
        self,
        user_repo: ports.VectorizedUserRepo,
        item_repo: ports.VectorizedItemRepo,
        batch_client: SwipeBatchClient,
        vector_processor_client: ports.VectorProcessorClient,
        batch_size: BatchSize
    ):
        self.__user_repo = user_repo
        self.__item_repo = item_repo
        self.__batch_client = batch_client
        self.__vector_processor_client = vector_processor_client
        self.__batch_size = batch_size

    async def apply_feedback(self, user_id: UUID, item_id: UUID, feedback: models.FeedbackType):
        user = await self.__user_repo.get_by_id(user_id)

        if user is None:
            raise errors.NotFoundError(f"user with id {user_id} not found")

        item = await self.__item_repo.get_by_id(item_id)

        if item is None:
            raise errors.NotFoundError(f"item with id {item_id} not found")

        await self.__batch_client.push_feedback(user_id, models.ItemFeedback(item, feedback))
        batch_size = await self.__batch_client.get_feedback_count(user_id)

        if self.__should_submit_batch(user, batch_size):
            await self.__submit_batch(user)

    def __should_submit_batch(self, user: models.VectorizedUser, batch_size: int):
        return (user.embedding.is_zero() and batch_size >= self.__batch_size.zero) or \
            (not user.embedding.is_zero() and batch_size >= self.__batch_size.default)

    async def __submit_batch(self, user: models.VectorizedUser):
        items = await self.__batch_client.get_feedback_items(user.user_id)
        new_embedding = await self.__vector_processor_client.adjust_user_embedding(user, items)
        user.embedding = new_embedding
        await self.__user_repo.update(user)
        await self.__batch_client.clear_feedback(user.user_id)
