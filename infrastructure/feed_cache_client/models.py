from uuid import UUID
from abc import ABCMeta, abstractmethod


class CachedItem(metaclass=ABCMeta):
    @property
    @abstractmethod
    def item_id(self) -> UUID:
        ...
