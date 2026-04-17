from core import errors


class EmbeddingError(errors.BaseError):
    def __init__(self, *args):
        super().__init__("embedding error", *args)
