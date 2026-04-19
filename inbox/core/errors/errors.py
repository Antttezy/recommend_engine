from core.errors import errors


class PayloadParseError(errors.BaseError):
    def __init__(self, *args):
        super().__init__("payload parsing error", *args)
