from vector_processor.core import ports, models


class DefaultUserEmbedder(ports.AsyncUserEmbedder):
    async def get_user_embedding(self, _):
        embedding = models.Embedding(data=[0.0] * models.Embedding.EMBEDDING_LENGTH)
        return embedding
