import abc

from vector_processor.core import models


class ItemEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_item_embedding(self, item: models.ItemInfo) -> models.Embedding:
        ...


class AsyncItemEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_item_embedding(self, item: models.ItemInfo) -> models.Embedding:
        ...
