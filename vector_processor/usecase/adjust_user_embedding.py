from vector_processor.core import ports, models


class AdjustUserEmbeddingUsecase:
    def __init__(self, user_adjuster: ports.AsyncUserAdjuster):
        self.__user_adjuster = user_adjuster

    async def adjust_user_embedding(self,
                                    user: models.Embedding,
                                    feedbacks: list[models.Feedback]):

        embedding = await self.__user_adjuster.adjust_user_embedding(user, feedbacks)
        return embedding
