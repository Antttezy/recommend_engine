from api.grpc.vector_processor import vector_processor_pb2


try:
    from grpc_reflection.v1alpha import reflection
except (ImportError, ModuleNotFoundError):
    reflection = None


def add_reflection(server):
    if reflection is not None:
        SERVICE_NAMES = [
            vector_processor_pb2.DESCRIPTOR.services_by_name["VectorProcessor"].full_name
        ]

        reflection.enable_server_reflection(SERVICE_NAMES, server)
