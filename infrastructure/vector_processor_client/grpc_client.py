from grpc import StatusCode
from grpc.aio import Channel, AioRpcError
from core.ports import VectorProcessorClient
from api.grpc.vector_processor import vector_processor_pb2, vector_processor_pb2_grpc
from .errors import VectorizationError
from .mapping import map_feedback_list, map_userupdate, map_itemupdate, map_vectorizeduser
from .mapping import reverse_map_embedding


class GrpcVectorProcessorClient(VectorProcessorClient):
    def __init__(self, channel: Channel):
        super().__init__()
        self.__channel = channel
        self.__stub = vector_processor_pb2_grpc.VectorProcessorStub(self.__channel)

    async def get_item_embedding(self, item):
        info = map_itemupdate(item)

        try:
            embedding: vector_processor_pb2.Embedding = await self.__stub.get_item_embedding(info)
            return reverse_map_embedding(embedding)
        except AioRpcError as e:
            if e.code() == StatusCode.INVALID_ARGUMENT:
                raise VectorizationError(e.details())
            else:
                raise e

    async def get_user_embedding(self, user):
        info = map_userupdate(user)

        try:
            embedding: vector_processor_pb2.Embedding = await self.__stub.get_user_embedding(info)
            return reverse_map_embedding(embedding)
        except AioRpcError as e:
            if e.code() == StatusCode.INVALID_ARGUMENT:
                raise VectorizationError(e.details())
            else:
                raise e

    async def adjust_user_embedding(self, user, feedbacks):
        r = vector_processor_pb2.AdjustUserRequest(
            user=map_vectorizeduser(user),
            feedbacks=map_feedback_list(feedbacks)
        )

        try:
            embedding: vector_processor_pb2.Embedding = await self.__stub.adjust_user_embedding(r)
            return reverse_map_embedding(embedding)
        except AioRpcError as e:
            if e.code() == StatusCode.INVALID_ARGUMENT:
                raise VectorizationError(e.details())
            else:
                raise e
