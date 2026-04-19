import asyncio
import logging
import signal

from grpc.aio import insecure_channel
from qdrant_client import AsyncQdrantClient

from infrastructure.vector_processor_client import new_grpc_vector_processor_client
from infrastructure.vectorized_item_repo import QdrantItemRepo
from infrastructure.vectorized_user_repo import QdrantUserRepo
from inbox import config, usecase
from inbox.adapters.update_handlers import ItemUpdateHandler, StockUpdateHandler, UserUpdateHandler
from inbox.kafka.poller import KafkaPoller
from inbox.kafka.const import ITEM_UPDATE_TOPIC, STOCK_UPDATE_TOPIC, USER_UPDATE_TOPIC


async def main():
    settings = config.load_config()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])
    logger = logging.getLogger(__name__)

    vector_channel = insecure_channel(settings.VECTOR_PROCESSOR_ENDPOINT)
    qdrant_client = AsyncQdrantClient(settings.QDRANT_URL)

    try:
        vector_processor = new_grpc_vector_processor_client(vector_channel)
        item_repo = QdrantItemRepo(qdrant_client)
        user_repo = QdrantUserRepo(qdrant_client)

        process_item_usecase = usecase.ProcessItemUsecase(vector_processor, item_repo)
        process_stock_usecase = usecase.ProcessStockUsecase(item_repo)
        process_user_usecase = usecase.ProcessUserUsecase(vector_processor, user_repo)

        handlers = {
            ITEM_UPDATE_TOPIC: ItemUpdateHandler(process_item_usecase),
            STOCK_UPDATE_TOPIC: StockUpdateHandler(process_stock_usecase),
            USER_UPDATE_TOPIC: UserUpdateHandler(process_user_usecase)
        }

        poller = KafkaPoller(settings.KAFKA_LISTENER, handlers)

        logging.info("Starting kafka poller...")
        await poller.start()

        loop = asyncio.get_running_loop()
        quit_event = asyncio.Event()

        async def shutdown():
            logging.info("Shutting down...")
            await poller.shutdown()
            quit_event.set()

        def sig_handler():
            asyncio.create_task(shutdown())

        loop.add_signal_handler(signal.SIGINT, sig_handler)
        loop.add_signal_handler(signal.SIGTERM, sig_handler)

        await quit_event.wait()
    finally:
        await qdrant_client.close()
        await vector_channel.close()


if __name__ == "__main__":
    asyncio.run(main())
