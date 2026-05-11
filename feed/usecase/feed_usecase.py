from uuid import UUID

from core import ports as coreports, errors
from feed.core import ports, models
from feed.core.errors import NoItemError


class FeedLimits:
    zero_embedding: int
    default: int


class FeedUsecase:
    def __init__(self, feed_cache: ports.FeedCacheClient,
                 item_recommend: coreports.ItemRecommend,
                 vectorized_user_repo: coreports.VectorizedUserRepo,
                 limits: FeedLimits):
        self.__feed_cache = feed_cache
        self.__item_recommend = item_recommend
        self.__vectorized_user_repo = vectorized_user_repo
        self.limits = limits

    async def show_item(self, user_id: UUID) -> models.FeedItem:
        item = await self.__feed_cache.get_next_item(user_id)

        if item is None:
            item = await self.__populate_cache(user_id)

        return models.FeedItem(item.item_id)

    async def next_item(self, user_id: UUID) -> models.FeedItem:
        await self.__feed_cache.pop_item(user_id)
        item = await self.__feed_cache.get_next_item(user_id)

        if item is None:
            item = await self.__populate_cache(user_id)

        return models.FeedItem(item.item_id)

    async def __populate_cache(self, user_id: UUID) -> models.CachedItem:
        user = await self.__vectorized_user_repo.get_by_id(user_id)

        if user is None:
            raise errors.NotFoundError(f"User {user_id} not found")

        limit = self.limits.zero_embedding if user.embedding.is_zero() else self.limits.default
        items = await self.__item_recommend.get_recommended(user, limit)

        if len(items) == 0:
            raise NoItemError("expected to get at least one recommended item")

        await self.__feed_cache.push_items(user_id, items)
        return items[0]
