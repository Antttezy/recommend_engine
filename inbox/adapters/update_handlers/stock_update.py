from inbox.core import errors, ports
from inbox.usecase import ProcessStockUsecase
from .parsers import parse_stock_update


class StockUpdateHandler(ports.UpdateHandler):
    def __init__(self, usecase: ProcessStockUsecase):
        super().__init__()
        self.__usecase = usecase

    async def handle(self, payload):
        if not isinstance(payload, bytes):
            raise errors.PayloadParseError("expected payload to be bytes")

        stock_update = await parse_stock_update(payload)
        await self.__usecase.process_stock(stock_update)
