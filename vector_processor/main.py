import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import grpc
import signal

from transformers import CLIPModel, CLIPProcessor

from api.grpc.vector_processor import vector_processor_pb2_grpc
from vector_processor import config, usecase
from vector_processor.adapters.vector_processor_service import VectorProcessorGrpcService
from vector_processor.adapters import mappers, async_item_embedder, item_embedder
from vector_processor.adapters import async_user_embedder
from vector_processor.adapters import async_user_adjuster, user_adjuster
from vector_processor.grpc_reflection import add_reflection


async def main():
    # Config and logging
    settings = config.load_config()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])

    # CPU-bound executor pool
    pool = ThreadPoolExecutor()

    # CLIP device
    ml_device = "cpu"

    # GRPC model mappers

    embedding_mapper = mappers.MapProtoEmbeddingEmbedding()
    item_info_mapper = mappers.MapItemInfoItemUpdate()
    user_info_mapper = mappers.MapUserInfoUserUpdate()
    feedback_mapper = mappers.MapFeedback(embedding_mapper)
    response_mapper = mappers.MapEmbeddingProtoEmbedding()

    # get_item_embedding dependencies
    itemEmbedder = item_embedder.ClipItemEmbedder(
        CLIPModel.from_pretrained(settings.CLIP_MODEL).to(ml_device),
        CLIPProcessor.from_pretrained(settings.CLIP_PROCESSOR),
        ml_device
    )

    asyncItemEmbedder = async_item_embedder.ItemEmbedderAsyncExecutor(itemEmbedder, pool)
    get_item_embedding_usecase = usecase.GetItemEmbeddingUsecase(asyncItemEmbedder)

    # get_user_embedding dependencies
    userEmbedder = async_user_embedder.DefaultUserEmbedder()
    get_user_embedding_usecase = usecase.GetUserEmbeddingUsecase(userEmbedder)

    # adjust_user_embedding dependencies
    userAdjuster = user_adjuster.FadingAvgUserAdjuster(
        settings.FEEDBACK_LIKE_LEARNING_RATE,
        settings.FEEDBACK_DISLIKE_LEARNING_RATE,
        settings.FEEDBACK_DECAY
    )

    asyncUserAdjuster = async_user_adjuster.UserAdjusterAsyncAdapter(userAdjuster)
    adjust_user_embedding_usecase = usecase.AdjustUserEmbeddingUsecase(asyncUserAdjuster)

    vector_processor = VectorProcessorGrpcService(
        item_info_mapper,
        user_info_mapper,
        feedback_mapper,
        embedding_mapper,
        response_mapper,
        get_item_embedding_usecase,
        get_user_embedding_usecase,
        adjust_user_embedding_usecase
    )

    grpc_server = grpc.aio.server()
    vector_processor_pb2_grpc.add_VectorProcessorServicer_to_server(vector_processor, grpc_server)

    if settings.GRPC_REFLECTION:
        logging.info("GRPC_REFLECTION is set, enabling reflection...")
        add_reflection(grpc_server)

    listen_addr = f"0.0.0.0:{settings.GRPC_PORT}"
    grpc_server.add_insecure_port(listen_addr)

    logging.info("Starting gRPC server...")
    await grpc_server.start()

    # Graceful shutdown setup
    loop = asyncio.get_running_loop()
    quit_event = asyncio.Event()

    async def shutdown():
        logging.info("Shutting down...")
        await grpc_server.stop(60.0)
        quit_event.set()

    def sig_handler():
        asyncio.create_task(shutdown())

    loop.add_signal_handler(signal.SIGINT, sig_handler)
    loop.add_signal_handler(signal.SIGTERM, sig_handler)

    await quit_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
