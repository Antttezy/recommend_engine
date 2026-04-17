from core import errors


class MappingError(errors.BaseError):
    def __init__(self, *args):
        super().__init__("entity mapping error", *args)
