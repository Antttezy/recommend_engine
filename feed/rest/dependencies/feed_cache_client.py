from fastapi import Depends
from valkey.asyncio import Valkey

from infrastructure.feed_cache_client import FeedCacheClient
from .valkey import get_valkey


def feed_cache_client(valkey: Valkey = Depends(get_valkey)):
    return FeedCacheClient(valkey)
