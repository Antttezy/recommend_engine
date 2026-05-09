import logging

from qdrant_client import AsyncQdrantClient
import uvicorn
from valkey.asyncio import ConnectionPool

from feed import config
from feed.rest import create_api


def main():
    settings = config.load_settings()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])

    valkey_pool = ConnectionPool.from_url(
        settings.VALKEY_URL, max_connections=20, decode_responses=True)
    qdrant_client = AsyncQdrantClient(settings.QDRANT_URL)

    api = create_api(settings, valkey_pool, qdrant_client)

    uvicorn.run(
        api,
        host='0.0.0.0',
        port=settings.HTTP_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
