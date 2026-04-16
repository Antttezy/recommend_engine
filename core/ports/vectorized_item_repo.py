import abc
from typing import Optional
import uuid

from core import models


class VectorizedItemRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_by_id(item_id: uuid.UUID) -> Optional[models.VectorizedItem]:
        ...

    @abc.abstractmethod
    async def add(vectorized_item: models.VectorizedItem):
        """:raises: :class:`errors.AlreadyExistsError`"""
        ...

    @abc.abstractmethod
    async def update(vectorized_item: models.VectorizedItem):
        """:raises: :class:`errors.NotFoundError`"""
        ...
