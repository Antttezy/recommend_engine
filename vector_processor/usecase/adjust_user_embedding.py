from core import models
from vector_processor.core import ports


class AdjustUserEmbeddingUsecase:
    def __init__(self, user_adjuster: ports.AsyncUserAdjuster):
        self.__user_adjuster = user_adjuster

    async def adjust_user_embedding(self,
                                    user: models.VectorizedUser,
                                    feedbacks: list[models.ItemFeedback]):

        embedding = await self.__user_adjuster.adjust_user_embedding(user, feedbacks)
        return embedding
