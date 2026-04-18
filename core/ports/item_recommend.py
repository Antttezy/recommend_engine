import abc

from core import models


class ItemRecommend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_recommended(self, user: models.VectorizedUser, limit: int) -> list[models.VectorizedItem]:
        ...
