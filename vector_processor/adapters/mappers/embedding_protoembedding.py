from api.grpc.vector_processor.vector_processor_pb2 import Embedding as Embedding_pb2
from core.models import Embedding
from vector_processor import mapper


class MapEmbeddingProtoEmbedding(mapper.MapperBase[Embedding, Embedding_pb2]):
    def mapItem(self, i):
        return Embedding_pb2(data=[x for x in i.data])


class MapProtoEmbeddingEmbedding(mapper.MapperBase[Embedding_pb2, Embedding]):
    def mapItem(self, i):
        return Embedding(data=[x for x in i.data])
