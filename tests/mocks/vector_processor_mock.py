import random
from core import ports, const, models


class VectorProcessorMock(ports.VectorProcessorClient):
    async def get_item_embedding(self, item):
        return models.Embedding([random.random() * 2 - 1 for _ in range(const.EMBEDDING_LENGTH)])

    async def get_user_embedding(self, user):
        return models.Embedding([0.0] * const.EMBEDDING_LENGTH)

    async def adjust_user_embedding(self, user, feedbacks):
        if len(feedbacks) == 0:
            return user.embedding

        return feedbacks[0].item.embedding
