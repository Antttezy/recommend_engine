import abc
from typing import Optional
import uuid

from core import models


class VectorizedUserRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_by_id(user_id: uuid.UUID) -> Optional[models.VectorizedUser]:
        ...

    @abc.abstractmethod
    async def add(vectorized_user: models.VectorizedUser):
        """:raises: :class:`errors.AlreadyExistsError`"""
        ...

    @abc.abstractmethod
    async def update(vectorized_user: models.VectorizedUser):
        """:raises: :class:`errors.NotFoundError`"""
        ...
