from core import models
from core.const import EMBEDDING_LENGTH
from vector_processor import ports


class DefaultUserEmbedder(ports.AsyncUserEmbedder):
    async def get_user_embedding(self, _):
        embedding = models.Embedding(data=[0.0] * EMBEDDING_LENGTH)
        return embedding
