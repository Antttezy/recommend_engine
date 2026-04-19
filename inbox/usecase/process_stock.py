from core import models, ports, const


class ProcessStockUsecase:
    def __init__(self, repo: ports.VectorizedItemRepo):
        self.repo = repo

    async def process_stock(self, stock: models.StockUpdate):
        stored_item = await self.repo.get_by_id(stock.item_id)
        in_stock = stock.amount > 0

        if stored_item is not None:
            stored_item.in_stock = in_stock
            await self.repo.update(stored_item)

        else:
            stored_item = models.VectorizedItem(
                item_id=stock.item_id,
                in_stock=in_stock,
                embedding_ready=False,
                sex=models.Gender.NOT_SPECIFIED,
                embedding=models.Embedding([0.0] * const.EMBEDDING_LENGTH)
            )

            await self.repo.add(stored_item)
