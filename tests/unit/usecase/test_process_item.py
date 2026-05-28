import uuid

import pytest

from core import const, models
from inbox.usecase import ProcessItemUsecase
from tests.mocks import VectorProcessorMock, VectorizedItemRepoMock
from tests.fixtures import image, random_embedding


@pytest.mark.asyncio
async def test_process_new_item(image):
    vector_processor = VectorProcessorMock()
    repo = VectorizedItemRepoMock()
    usecase = ProcessItemUsecase(vector_processor, repo)

    update = models.ItemUpdate(
        item_id=uuid.uuid4(),
        name="ItemName",
        price=42.0,
        description="ItemDescription",
        attributes={'attr': 21},
        photos=[models.Photo(image)],
        sex=models.Gender.FEMALE
    )

    await usecase.process_item(update)

    item = await repo.get_by_id(update.item_id)
    assert item is not None
    assert item.item_id == update.item_id
    assert not item.embedding.is_zero()
    assert item.embedding_ready
    assert item.ready
    assert not item.in_stock
    assert item.sex == models.Gender.FEMALE


@pytest.mark.asyncio
async def test_process_existing_item(image, random_embedding):
    vector_processor = VectorProcessorMock()
    repo = VectorizedItemRepoMock()
    usecase = ProcessItemUsecase(vector_processor, repo)

    item_id = uuid.uuid4()
    await repo.add(models.VectorizedItem(
        item_id=item_id,
        in_stock=False,
        embedding_ready=True,
        sex=models.Gender.FEMALE,
        embedding=random_embedding
    ))

    update = models.ItemUpdate(
        item_id=item_id,
        name="ItemName",
        price=42.0,
        description="ItemDescription",
        attributes={'attr': 21},
        photos=[models.Photo(image)],
        sex=models.Gender.MALE
    )

    await usecase.process_item(update)
    item = await repo.get_by_id(item_id)
    assert item is not None
    assert item.item_id == item_id
    assert item.embedding != random_embedding
    assert item.embedding_ready
    assert item.ready
    assert not item.in_stock
    assert item.sex == models.Gender.MALE


@pytest.mark.asyncio
async def test_process_not_ready_item(image):
    vector_processor = VectorProcessorMock()
    repo = VectorizedItemRepoMock()
    usecase = ProcessItemUsecase(vector_processor, repo)

    item_id = uuid.uuid4()
    await repo.add(models.VectorizedItem(
        item_id=item_id,
        in_stock=True,
        embedding_ready=False,
        sex=models.Gender.NOT_SPECIFIED,
        embedding=models.Embedding([0.0] * const.EMBEDDING_LENGTH)
    ))

    update = models.ItemUpdate(
        item_id=item_id,
        name="ItemName",
        price=42.0,
        description="ItemDescription",
        attributes={'attr': 21},
        photos=[models.Photo(image)],
        sex=models.Gender.FEMALE
    )

    await usecase.process_item(update)
    item = await repo.get_by_id(item_id)
    assert item is not None
    assert item.item_id == item_id
    assert not item.embedding.is_zero()
    assert item.embedding_ready
    assert item.ready
    assert item.in_stock
    assert item.sex == models.Gender.FEMALE
