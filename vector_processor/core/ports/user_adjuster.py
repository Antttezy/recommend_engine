import abc

from vector_processor.core import models


class UserAdjuster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def adjust_user_embedding(
            self,
            user: models.Embedding,
            feedbacks: list[models.Feedback]) -> models.Embedding:
        ...


class AsyncUserAdjuster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def adjust_user_embedding(
            self,
            user: models.Embedding,
            feedbacks: list[models.Feedback]) -> models.Embedding:
        ...
