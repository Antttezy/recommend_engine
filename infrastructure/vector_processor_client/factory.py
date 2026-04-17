import grpc.aio
from .grpc_client import GrpcVectorProcessorClient


def new_grpc_vector_processor_client(channel: grpc.aio.Channel) -> GrpcVectorProcessorClient:
    return GrpcVectorProcessorClient(channel)
