import uuid

import pytest

from core import models
from core.errors import NotFoundError
from tests.fixtures import random_embedding, zero_embedding
from tests import mocks

from feed.core.models import CachedItem
from feed.core.errors import NoItemError
from feed.usecase import FeedUsecase, FeedLimits


@pytest.mark.asyncio
async def test_show_item_empty_cache_nonzero(random_embedding):
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, random_embedding)

    repo = mocks.VectorizedUserRepoMock()
    await repo.add(user)

    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.show_item(user_id)
    item2 = await usecase.show_item(user_id)

    assert item is not None
    assert item2 is not None
    assert item.item_id == item2.item_id

    info = next(filter(lambda i: i.item_id == item.item_id, recommend.item_pool))
    assert info.sex == models.Gender.NOT_SPECIFIED or info.sex == user.sex

    assert len(cache.storage[user_id]) == limits.default


@pytest.mark.asyncio
async def test_show_item_empty_cache_zero(zero_embedding):
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, zero_embedding)

    repo = mocks.VectorizedUserRepoMock()
    await repo.add(user)

    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.show_item(user_id)
    item2 = await usecase.show_item(user_id)

    assert item is not None
    assert item2 is not None
    assert item.item_id == item2.item_id

    info = next(filter(lambda i: i.item_id == item.item_id, recommend.item_pool))
    assert info.sex == models.Gender.NOT_SPECIFIED or info.sex == user.sex

    assert len(cache.storage[user_id]) == limits.zero_embedding


@pytest.mark.asyncio
async def test_show_item_nonempty_cache(zero_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, zero_embedding)

    repo = mocks.VectorizedUserRepoMock()
    cache = mocks.FeedCacheClientMock()
    recommend = mocks.FailingItemRecommendMock()
    limits = FeedLimits()

    await repo.add(user)
    await cache.push_items(user_id, [CachedItem(item_id), CachedItem(uuid.uuid4())])
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.show_item(user_id)
    item2 = await usecase.show_item(user_id)

    assert item is not None
    assert item2 is not None
    assert item.item_id == item2.item_id == item_id


@pytest.mark.asyncio
async def test_next_item_empty_cache(random_embedding):
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, random_embedding)

    repo = mocks.VectorizedUserRepoMock()
    await repo.add(user)

    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.next_item(user_id)
    show = await usecase.show_item(user_id)
    item2 = await usecase.next_item(user_id)
    show2 = await usecase.show_item(user_id)

    assert item is not None
    assert show is not None
    assert item2 is not None
    assert show2 is not None
    assert item.item_id == show.item_id
    assert item2.item_id == show2.item_id
    assert item.item_id != item2.item_id

    info = next(filter(lambda i: i.item_id == item.item_id, recommend.item_pool))
    info2 = next(filter(lambda i: i.item_id == item2.item_id, recommend.item_pool))
    assert info.sex == models.Gender.NOT_SPECIFIED or info.sex == user.sex
    assert info2.sex == models.Gender.NOT_SPECIFIED or info2.sex == user.sex

    assert len(cache.storage[user_id]) == limits.default - 1


@pytest.mark.asyncio
async def test_next_item_nonempty_cache(zero_embedding):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, zero_embedding)

    repo = mocks.VectorizedUserRepoMock()
    cache = mocks.FeedCacheClientMock()
    recommend = mocks.FailingItemRecommendMock()
    limits = FeedLimits()

    await repo.add(user)
    await cache.push_items(user_id, [CachedItem(uuid.uuid4()), CachedItem(item_id)])
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.next_item(user_id)
    item2 = await usecase.show_item(user_id)

    assert item is not None
    assert item2 is not None
    assert item.item_id == item2.item_id == item_id


@pytest.mark.asyncio
async def test_next_item_one_item_in_cache(random_embedding):
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, random_embedding)

    repo = mocks.VectorizedUserRepoMock()
    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()

    await repo.add(user)
    await cache.push_items(user_id, [CachedItem(uuid.uuid4())])
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)
    item = await usecase.next_item(user_id)

    assert item is not None
    assert len(cache.storage[user_id]) == limits.default


@pytest.mark.asyncio
async def test_missing_user():
    user_id = uuid.uuid4()

    repo = mocks.VectorizedUserRepoMock()
    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)

    try:
        await usecase.show_item(user_id)
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected to get NotFoundError")


@pytest.mark.asyncio
async def test_no_items(random_embedding):
    user_id = uuid.uuid4()
    user = models.VectorizedUser(user_id, models.Gender.FEMALE, random_embedding)

    repo = mocks.VectorizedUserRepoMock()
    cache = mocks.FeedCacheClientMock()
    recommend = mocks.ItemRecommendMock()
    limits = FeedLimits()

    await repo.add(user)
    recommend.item_pool.clear()
    limits.default = 5
    limits.zero_embedding = 1

    usecase = FeedUsecase(cache, recommend, repo, limits)

    try:
        await usecase.show_item(user_id)
    except NoItemError:
        pass
    else:
        pytest.fail("Expected to get NoItemError")
