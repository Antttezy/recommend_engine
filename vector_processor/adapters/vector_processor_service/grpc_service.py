import grpc.aio as grpc

from api.grpc.vector_processor import vector_processor_pb2_grpc
from api.grpc.vector_processor import vector_processor_pb2
from core import models
from vector_processor import mapper, usecase


class VectorProcessorGrpcService(vector_processor_pb2_grpc.VectorProcessorServicer):
    def __init__(
            self,
            item_info_mapper: mapper.MapperBase[vector_processor_pb2.ItemInfo, models.ItemUpdate],
            user_info_mapper: mapper.MapperBase[vector_processor_pb2.UserInfo, models.UserUpdate],
            feedback_mapper: mapper.MapperBase[vector_processor_pb2.AdjustUserRequest.Feedback, models.ItemFeedback],
            vec_user_mapper: mapper.MapperBase[vector_processor_pb2.Embedding, models.VectorizedUser],
            response_mapper: mapper.MapperBase[models.Embedding, vector_processor_pb2.Embedding],
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
        _: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:
        item = self.__item_info_mapper.mapItem(request)
        embedding = await self.__get_item_embedding_usecase.get_item_embedding(item)
        return self.__response_mapper.mapItem(embedding)

    async def get_user_embedding(
        self,
        request: vector_processor_pb2.UserInfo,
        _: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:
        user = self.__user_info_mapper.mapItem(request)
        embedding = await self.__get_user_embedding_usecase.get_user_embedding(user)
        return self.__response_mapper.mapItem(embedding)

    async def adjust_user_embedding(
        self,
        request: vector_processor_pb2.AdjustUserRequest,
        _: grpc.ServicerContext
    ) -> vector_processor_pb2.Embedding:
        user = self.__vec_user_mapper.mapItem(request.user)
        feedbacks: list[models.ItemFeedback] = []

        for f in request.feedbacks:
            feedbacks.append(self.__feedback_mapper.mapItem(f))

        embedding = await self.__adj_user_embedding_usecase.adjust_user_embedding(user, feedbacks)
        return self.__response_mapper.mapItem(embedding)
