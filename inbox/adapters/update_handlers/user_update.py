from inbox.core import errors, ports
from inbox.usecase import ProcessUserUsecase
from .parsers import parse_user_update


class UserUpdateHandler(ports.UpdateHandler):
    def __init__(self, usecase: ProcessUserUsecase):
        super().__init__()
        self.__usecase = usecase

    async def handle(self, payload):
        if not isinstance(payload, bytes):
            raise errors.PayloadParseError("expected payload to be bytes")

        user_update = await parse_user_update(payload)
        await self.__usecase.process_user(user_update)
