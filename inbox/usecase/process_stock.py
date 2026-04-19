from core import models, ports, errors


class ProcessStockUsecase:
    def __init__(self, repo: ports.VectorizedItemRepo):
        self.repo = repo

    async def process_stock(self, stock: models.StockUpdate):
        stored_item = await self.repo.get_by_id(stock.item_id)
        in_stock = stock.amount > 0

        if stored_item is None:
            # TODO: Partial update with ready=False in payload
            raise errors.NotFoundError("process stock", f"item_id={stock.item_id} not found")

        stored_item.in_stock = in_stock
        await self.repo.update(stored_item)
