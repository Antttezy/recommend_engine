import uuid

import pytest

from core import models
from core.errors import NotFoundError
from tests.fixtures import random_embedding, zero_embedding
from tests import mocks

from swipe_feedback.usecase import FeedbackUsecase, BatchSize


@pytest.mark.asyncio
async def test_first_feedback(zero_embedding, random_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    item = models.VectorizedItem(item_id, True, True, models.Gender.MALE, random_embedding)
    user = models.VectorizedUser(user_id, models.Gender.MALE, zero_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    batch_size = BatchSize(5, 10)

    await user_repo.add(user)
    await item_repo.add(item)

    usecase = FeedbackUsecase(user_repo, item_repo, batch, None, batch_size)
    await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)
    await usecase.apply_feedback(user_id, item_id, models.FeedbackType.NEGATIVE)

    assert len(batch.storage[user_id]) == 2
    assert batch.storage[user_id][0].feedback == models.FeedbackType.NEGATIVE
    assert batch.storage[user_id][1].feedback == models.FeedbackType.POSITIVE


@pytest.mark.asyncio
async def test_apply_feedback_nonzero_user_emb(random_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    item = models.VectorizedItem(item_id, True, True, models.Gender.MALE, random_embedding)
    user = models.VectorizedUser(user_id, models.Gender.MALE, random_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    batch_size = BatchSize(5, 10)

    await user_repo.add(user)
    await item_repo.add(item)

    for _ in range(4):
        await batch.push_feedback(user_id, models.ItemFeedback(item, models.FeedbackType.POSITIVE))

    usecase = FeedbackUsecase(user_repo, item_repo, batch, None, batch_size)
    await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)

    assert len(batch.storage[user_id]) == 5


@pytest.mark.asyncio
async def test_submit(zero_embedding, random_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    item = models.VectorizedItem(item_id, True, True, models.Gender.MALE, random_embedding)
    user = models.VectorizedUser(user_id, models.Gender.MALE, zero_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    vector = mocks.VectorProcessorMock()
    batch_size = BatchSize(5, 10)

    await user_repo.add(user)
    await item_repo.add(item)

    for _ in range(4):
        await batch.push_feedback(user_id, models.ItemFeedback(item, models.FeedbackType.POSITIVE))

    usecase = FeedbackUsecase(user_repo, item_repo, batch, vector, batch_size)
    await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)
    new_user = await user_repo.get_by_id(user_id)

    assert len(batch.storage[user_id]) == 0
    assert new_user.embedding.data == item.embedding.data


@pytest.mark.asyncio
async def test_submit_nonzero(zero_embedding, random_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    item = models.VectorizedItem(item_id, True, True, models.Gender.MALE, random_embedding)
    user = models.VectorizedUser(user_id, models.Gender.MALE, zero_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    vector = mocks.VectorProcessorMock()
    batch_size = BatchSize(5, 10)

    await user_repo.add(user)
    await item_repo.add(item)

    for _ in range(9):
        await batch.push_feedback(user_id, models.ItemFeedback(item, models.FeedbackType.POSITIVE))

    usecase = FeedbackUsecase(user_repo, item_repo, batch, vector, batch_size)
    await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)
    new_user = await user_repo.get_by_id(user_id)

    assert len(batch.storage[user_id]) == 0
    assert new_user.embedding.data == item.embedding.data


@pytest.mark.asyncio
async def test_missing_user(random_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    item = models.VectorizedItem(item_id, True, True, models.Gender.MALE, random_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    vector = mocks.VectorProcessorMock()
    batch_size = BatchSize(5, 10)

    await item_repo.add(item)

    usecase = FeedbackUsecase(user_repo, item_repo, batch, vector, batch_size)

    try:
        await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected to get NotFoundError")


@pytest.mark.asyncio
async def test_missing_item(zero_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.MALE, zero_embedding)

    item_repo = mocks.VectorizedItemRepoMock()
    user_repo = mocks.VectorizedUserRepoMock()
    batch = mocks.SwipeBatchClientMock()
    vector = mocks.VectorProcessorMock()
    batch_size = BatchSize(5, 10)

    await user_repo.add(user)

    usecase = FeedbackUsecase(user_repo, item_repo, batch, vector, batch_size)

    try:
        await usecase.apply_feedback(user_id, item_id, models.FeedbackType.POSITIVE)
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected to get NotFoundError")
