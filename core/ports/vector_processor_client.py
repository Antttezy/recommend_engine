import abc

from core import models


class VectorProcessorClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_item_embedding(self, item: models.ItemUpdate) -> models.Embedding:
        """Creates embedding for `ItemUpdate`"""
        ...

    @abc.abstractmethod
    async def get_user_embedding(self, user: models.UserUpdate) -> models.Embedding:
        """Creates embedding for `UserUpdate`"""
        ...

    @abc.abstractmethod
    async def adjust_user_embedding(
            self,
            user: models.VectorizedUser,
            feedbacks: list[models.ItemFeedback]) -> models.Embedding:
        """
        Creates new embedding based on existing user embedding and provided item feedback info

        :param user: existing user
        :param feedbacks: a list of user's feedback to items

        :returns: a new adjusted embedding for :param:`user`"""
        ...
