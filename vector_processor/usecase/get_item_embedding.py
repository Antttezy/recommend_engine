from core import models
from vector_processor.core import ports


class GetItemEmbeddingUsecase:
    def __init__(self, item_embedder: ports.AsyncItemEmbedder):
        self.__item_embedder = item_embedder

    async def get_item_embedding(self, item: models.ItemUpdate) -> models.Embedding:
        embedding = await self.__item_embedder.get_item_embedding(item)
        return embedding
