from vector_processor.core import ports, models


class GetUserEmbeddingUsecase:
    def __init__(self, user_embedder: ports.AsyncUserEmbedder):
        self.__user_embedder = user_embedder

    async def get_user_embedding(self, user: models.UserInfo) -> models.Embedding:
        embedding = await self.__user_embedder.get_user_embedding(user)
        return embedding
