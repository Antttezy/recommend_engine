import uuid

from core import models, ports


class VectorizedItemRepoMock(ports.VectorizedItemRepo):
    def __init__(self):
        self.items = dict[uuid.UUID, models.VectorizedItem]()

    async def add(self, vectorized_item):
        assert self.items.get(vectorized_item.item_id) is None
        self.items[vectorized_item.item_id] = vectorized_item

    async def update(self, vectorized_item):
        assert self.items.get(vectorized_item.item_id) is not None
        self.items[vectorized_item.item_id] = vectorized_item

    async def get_by_id(self, item_id):
        return self.items.get(item_id)
