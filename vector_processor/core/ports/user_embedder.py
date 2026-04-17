import abc

from vector_processor.core import models


class UserEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_user_embedding(self, user: models.UserInfo) -> models.Embedding:
        ...


class AsyncUserEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_user_embedding(self, user: models.UserInfo) -> models.Embedding:
        ...
