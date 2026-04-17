import asyncio
from concurrent.futures import Executor

from vector_processor.core import ports


class ItemEmbedderAsyncExecutor(ports.AsyncItemEmbedder):
    def __init__(self, item_embedder: ports.ItemEmbedder, pool: Executor):
        super().__init__()
        self.__item_embedder = item_embedder
        self.__pool = pool

    async def get_item_embedding(self, item):
        loop = asyncio.get_running_loop()

        embedding = await loop.run_in_executor(
            self.__pool,
            self.__item_embedder.get_item_embedding,
            item
        )

        return embedding
