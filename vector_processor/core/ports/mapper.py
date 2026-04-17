import abc


class Mapper[Tin, Tout](metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def mapItem(self, i: Tin) -> Tout:
        """
        Converts :param:`i` to :class:`Tout`

        :raises: :class:`..errors.MappingError`
        """
        ...
