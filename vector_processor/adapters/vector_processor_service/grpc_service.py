import grpc.aio as grpc
from grpc import StatusCode

from api.grpc.vector_processor import vector_processor_pb2_grpc
from api.grpc.vector_processor import vector_processor_pb2
from core import models
from vector_processor import usecase
from vector_processor.core import ports, errors


class VectorProcessorGrpcService(vector_processor_pb2_grpc.VectorProcessorServicer):
    def __init__(
            self,
            item_info_mapper: ports.Mapper[vector_processor_pb2.ItemInfo, models.ItemUpdate],
            user_info_mapper: ports.Mapper[vector_processor_pb2.UserInfo, models.UserUpdate],
            feedback_mapper: ports.Mapper[vector_processor_pb2.AdjustUserRequest.Feedback, models.ItemFeedback],
            vec_user_mapper: ports.Mapper[vector_processor_pb2.Embedding, models.VectorizedUser],
            response_mapper: ports.Mapper[models.Embedding, vector_processor_pb2.Embedding],
            get_item_embedding_usecase: usecase.GetItemEmbeddingUsecase,
            get_user_embedding_usecase: usecase.GetUserEmbeddingUsecase,
            adj_user_embedding_usecase: usecase.AdjustUserEmbeddingUsecase,
    ):
        super().__init__()

        self.__item_info_mapper = item_info_mapper
        self.__user_info_mapper = user_info_mapper
        self.__feedback_mapper = feedback_mapper
        self.__vec_user_mapper = vec_user_mapper
        self.__response_mapper = response_mapper
        self.__get_item_embedding_usecase = get_item_embedding_usecase
        self.__get_user_embedding_usecase = get_user_embedding_usecase
        self.__adj_user_embedding_usecase = adj_user_embedding_usecase

    async def get_item_embedding(
        self,
        request: vector_processor_pb2.ItemInfo,
        ctx: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:

        try:
            item = self.__item_info_mapper.mapItem(request)
        except errors.MappingError as e:
            err = ": ".join(["could not map request", *e.args])
            await ctx.abort(StatusCode.INVALID_ARGUMENT, err)

        embedding = await self.__get_item_embedding_usecase.get_item_embedding(item)
        return self.__response_mapper.mapItem(embedding)

    async def get_user_embedding(
        self,
        request: vector_processor_pb2.UserInfo,
        ctx: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:

        try:
            user = self.__user_info_mapper.mapItem(request)
        except errors.MappingError as e:
            err = ": ".join(["could not map request", *e.args])
            await ctx.abort(StatusCode.INVALID_ARGUMENT, err)

        embedding = await self.__get_user_embedding_usecase.get_user_embedding(user)
        return self.__response_mapper.mapItem(embedding)

    async def adjust_user_embedding(
        self,
        request: vector_processor_pb2.AdjustUserRequest,
        ctx: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:

        try:
            user = self.__vec_user_mapper.mapItem(request.user)
            feedbacks: list[models.ItemFeedback] = []

            for f in request.feedbacks:
                feedbacks.append(self.__feedback_mapper.mapItem(f))
        except errors.MappingError as e:
            err = ": ".join(["could not map request", *e.args])
            await ctx.abort(StatusCode.INVALID_ARGUMENT, err)

        embedding = await self.__adj_user_embedding_usecase.adjust_user_embedding(user, feedbacks)
        return self.__response_mapper.mapItem(embedding)
