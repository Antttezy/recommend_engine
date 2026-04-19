import asyncio
import logging

from qdrant_client import AsyncQdrantClient
from infrastructure.qdrant.migration import QdrantMigrator

from .config import Settings


async def main():
    settings = Settings()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])

    client = AsyncQdrantClient(settings.QDRANT_URL, prefer_grpc=True)

    try:
        logging.info("Connecting to qdrant...")
        info = await client.info()
        logging.info("Connected to %s %s", info.title, info.version)
        
        logging.info("Creating collections...")
        migrator = QdrantMigrator(client)
        await migrator.create_collections_if_needed()
        logging.info("Collections created")
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())
