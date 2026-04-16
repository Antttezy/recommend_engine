import abc


class MapperBase[Tin, Tout](metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def mapItem(self, i: Tin) -> Tout:
        ...
