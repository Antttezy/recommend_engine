from api.grpc.vector_processor.vector_processor_pb2 import Embedding as Embedding_pb2
from core.models import Embedding
from vector_processor.core import ports, errors


class MapEmbeddingProtoEmbedding(ports.Mapper[Embedding, Embedding_pb2]):
    def mapItem(self, i):
        return Embedding_pb2(data=[x for x in i.data])


class MapProtoEmbeddingEmbedding(ports.Mapper[Embedding_pb2, Embedding]):
    def mapItem(self, i):
        try:
            return Embedding(data=[x for x in i.data])
        except:
            raise errors.MappingError("embedding")
