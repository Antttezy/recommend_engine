import abc

from core import models


class UserAdjuster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def adjust_user_embedding(
            self,
            user: models.VectorizedUser,
            feedbacks: list[models.ItemFeedback]) -> models.Embedding:
        ...


class AsyncUserAdjuster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def adjust_user_embedding(
            self,
            user: models.VectorizedUser,
            feedbacks: list[models.ItemFeedback]) -> models.Embedding:
        ...
