from fastapi import Request
from valkey.asyncio import Valkey


async def get_valkey(request: Request):
    valkey_pool = request.app.state.valkey_pool

    async with Valkey(connection_pool=valkey_pool) as valkey:
        yield valkey
