from core import models, ports


class ProcessItemUsecase:
    def __init__(self,
                 vector_processor: ports.VectorProcessorClient,
                 repo: ports.VectorizedItemRepo):
        self.vector_processor = vector_processor
        self.repo = repo

    async def process_item(self, item: models.ItemUpdate):
        embedding = await self.vector_processor.get_item_embedding(item)
        stored_item = await self.repo.get_by_id(item.item_id)

        if stored_item is not None:
            stored_item.embedding = embedding
            stored_item.sex = item.sex
            await self.repo.update(stored_item)

        else:
            stored_item = models.VectorizedItem(
                item_id=item.item_id,
                in_stock=False,
                sex=item.sex,
                embedding=embedding
            )

            await self.repo.add(stored_item)
