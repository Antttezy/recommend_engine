from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core import errors, ports as coreports
from feed.core import ports
from feed.core.errors import NoItemError
from feed.rest import schema, dependencies
from feed.usecase import FeedUsecase, FeedLimits


router = APIRouter(tags=['item feed'])


@router.get("/show", response_model=schema.FeedItemResponse, responses=schema.feed_show_item_responses)
async def show_item(user_id: UUID = Depends(dependencies.authenticated_user_id),
                    feed_cache: ports.FeedCacheClient = Depends(dependencies.feed_cache_client),
                    user_repo: coreports.VectorizedItemRepo = Depends(dependencies.user_repo),
                    item_recommend: coreports.ItemRecommend = Depends(dependencies.item_recommend),
                    limitsdict: dict[str, int] = Depends(dependencies.feed_limits)):
    limits = FeedLimits()
    limits.zero_embedding = limitsdict['zero']
    limits.default = limitsdict['default']

    usecase = FeedUsecase(feed_cache, item_recommend, user_repo, limits)

    try:
        item = await usecase.show_item(user_id)
        return schema.FeedItemResponse(id=item.item_id)
    except errors.NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
    except NoItemError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'no items available')


@router.post("/next", response_model=schema.FeedItemResponse, responses=schema.feed_show_item_responses)
async def next_item(user_id: UUID = Depends(dependencies.authenticated_user_id),
                    feed_cache: ports.FeedCacheClient = Depends(dependencies.feed_cache_client),
                    user_repo: coreports.VectorizedItemRepo = Depends(dependencies.user_repo),
                    item_recommend: coreports.ItemRecommend = Depends(dependencies.item_recommend),
                    limitsdict: dict[str, int] = Depends(dependencies.feed_limits)):
    limits = FeedLimits()
    limits.zero_embedding = limitsdict['zero']
    limits.default = limitsdict['default']

    usecase = FeedUsecase(feed_cache, item_recommend, user_repo, limits)
    item = await usecase.next_item(user_id)

    return schema.FeedItemResponse(id=item.item_id)
