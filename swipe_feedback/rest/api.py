from contextlib import asynccontextmanager

from fastapi import FastAPI
from grpc.aio import insecure_channel
from qdrant_client import AsyncQdrantClient
from valkey.asyncio import ConnectionPool

from swipe_feedback.config import Settings

from .controllers import feedback_router_v1


def create_api(config: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        valkey_pool = ConnectionPool.from_url(
            config.VALKEY_URL, max_connections=20, decode_responses=True)
        qdrant = AsyncQdrantClient(config.QDRANT_URL)
        vector_processor_channel = insecure_channel(config.VECTOR_PROCESSOR_ENDPOINT)

        app.state.config = config
        app.state.valkey_pool = valkey_pool
        app.state.qdrant = qdrant
        app.state.vector_processor_channel = vector_processor_channel

        yield
        await vector_processor_channel.close()
        await qdrant.close()
        await valkey_pool.aclose()

    app = FastAPI(
        title='Feedback Service',
        version='0.0.0',
        lifespan=lifespan
    )

    app.include_router(feedback_router_v1, prefix='/api/v1/feedback')
    return app
