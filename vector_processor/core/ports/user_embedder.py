import abc

from core import models


class UserEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_user_embedding(self, user: models.UserUpdate) -> models.Embedding:
        ...


class AsyncUserEmbedder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_user_embedding(self, user: models.UserUpdate) -> models.Embedding:
        ...
