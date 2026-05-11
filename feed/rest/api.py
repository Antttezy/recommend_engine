from contextlib import asynccontextmanager

from fastapi import FastAPI
from qdrant_client import AsyncQdrantClient
from valkey.asyncio import ConnectionPool

from feed.config import Settings

from .controllers import feed_router_v1


def create_api(config: Settings, valkey_pool: ConnectionPool, qdrant: AsyncQdrantClient):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.config = config
        app.state.qdrant = qdrant
        app.state.valkey_pool = valkey_pool
        yield
        await valkey_pool.aclose()
        await qdrant.close()

    app = FastAPI(
        title='Feed Service',
        version='0.0.0',
        lifespan=lifespan
    )

    app.include_router(feed_router_v1, prefix='/api/v1/feed')
    return app
