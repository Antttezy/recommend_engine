from api.grpc.vector_processor.vector_processor_pb2 import Embedding
from vector_processor.core import models
from vector_processor.core import ports, errors


class MapEmbeddingProtoEmbedding(ports.Mapper[models.Embedding, Embedding]):
    def mapItem(self, i):
        return Embedding(data=[x for x in i.data])


class MapProtoEmbeddingEmbedding(ports.Mapper[Embedding, models.Embedding]):
    def mapItem(self, i):
        try:
            return models.Embedding(data=[x for x in i.data])
        except:
            raise errors.MappingError("embedding")
