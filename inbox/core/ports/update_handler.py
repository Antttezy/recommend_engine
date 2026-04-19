import abc
from typing import Any


class UpdateHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def handle(self, payload: Any):
        ...
