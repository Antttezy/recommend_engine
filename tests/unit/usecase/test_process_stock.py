import uuid

import pytest

from core import models
from inbox.usecase import ProcessStockUsecase
from tests.mocks import VectorizedItemRepoMock
from tests.fixtures import random_embedding, zero_embedding


@pytest.mark.asyncio
async def test_process_new():
    repo = VectorizedItemRepoMock()
    usecase = ProcessStockUsecase(repo)

    update = models.StockUpdate(
        item_id=uuid.uuid4(),
        amount=1
    )

    await usecase.process_stock(update)

    item = await repo.get_by_id(update.item_id)
    assert item is not None
    assert item.item_id == update.item_id
    assert item.embedding.is_zero()
    assert not item.embedding_ready
    assert not item.ready
    assert item.in_stock
    assert item.sex == models.Gender.NOT_SPECIFIED


@pytest.mark.asyncio
async def test_process_existing_notready(zero_embedding):
    repo = VectorizedItemRepoMock()
    usecase = ProcessStockUsecase(repo)
    item_id = uuid.uuid4()

    await repo.add(models.VectorizedItem(
        item_id=item_id,
        in_stock=True,
        embedding_ready=False,
        sex=models.Gender.NOT_SPECIFIED,
        embedding=zero_embedding
    ))

    update = models.StockUpdate(
        item_id=item_id,
        amount=0
    )

    await usecase.process_stock(update)

    item = await repo.get_by_id(update.item_id)
    assert item is not None
    assert item.item_id == item_id
    assert item.embedding.is_zero()
    assert not item.embedding_ready
    assert not item.ready
    assert not item.in_stock
    assert item.sex == models.Gender.NOT_SPECIFIED


@pytest.mark.asyncio
async def test_process_existing_ready(random_embedding):
    repo = VectorizedItemRepoMock()
    usecase = ProcessStockUsecase(repo)
    item_id = uuid.uuid4()

    await repo.add(models.VectorizedItem(
        item_id=item_id,
        in_stock=False,
        embedding_ready=True,
        sex=models.Gender.MALE,
        embedding=random_embedding
    ))

    update = models.StockUpdate(
        item_id=item_id,
        amount=15
    )

    await usecase.process_stock(update)

    item = await repo.get_by_id(update.item_id)
    assert item is not None
    assert item.item_id == item_id
    assert not item.embedding.is_zero()
    assert item.embedding_ready
    assert item.ready
    assert item.in_stock
    assert item.sex == models.Gender.MALE
