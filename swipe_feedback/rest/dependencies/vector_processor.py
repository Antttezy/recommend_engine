from fastapi import Request
from infrastructure.vector_processor_client import new_grpc_vector_processor_client


def vector_processor_client(request: Request):
    channel = request.app.state.vector_processor_channel
    return new_grpc_vector_processor_client(channel)
