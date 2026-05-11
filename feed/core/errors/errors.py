from core import errors


class NoItemError(errors.BaseError):
    def __init__(self, *args):
        super().__init__("No item available", *args)
