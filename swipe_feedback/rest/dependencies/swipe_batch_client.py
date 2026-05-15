from fastapi import Depends
from valkey.asyncio import Valkey

from infrastructure.swipe_batch_client import SwipeBatchClient
from .valkey import get_valkey


def swipe_batch_client(valkey: Valkey = Depends(get_valkey)):
    return SwipeBatchClient(valkey)
