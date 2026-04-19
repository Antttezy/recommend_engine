from inbox.core import errors, ports
from inbox.usecase import ProcessItemUsecase
from .parsers import parse_item_update


class ItemUpdateHandler(ports.UpdateHandler):
    def __init__(self, usecase: ProcessItemUsecase):
        super().__init__()
        self.__usecase = usecase

    async def handle(self, payload):
        if not isinstance(payload, bytes):
            raise errors.PayloadParseError("expected payload to be bytes")

        item_update = await parse_item_update(payload)
        await self.__usecase.process_item(item_update)
