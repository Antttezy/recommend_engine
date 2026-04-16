import uuid

from api.grpc.vector_processor.vector_processor_pb2 import AdjustUserRequest, Embedding as Emb_pb2
from core.models import ItemFeedback, Embedding, VectorizedItem, Gender, FeedbackType, VectorizedUser
from vector_processor import mapper


class MapFeedback(mapper.MapperBase[AdjustUserRequest.Feedback, ItemFeedback]):
    def __init__(self, embedding: mapper.MapperBase[Emb_pb2, Embedding]):
        super().__init__()
        self.embedding = embedding

    def mapItem(self, i):
        feedback: FeedbackType

        if i.feedback == AdjustUserRequest.FeedbackType.POSITIVE:
            feedback = FeedbackType.POSITIVE
        else:
            feedback = FeedbackType.NEGATIVE

        return ItemFeedback(
            item=VectorizedItem(
                item_id=uuid.UUID(int=0),
                in_stock=True,
                sex=Gender.NOT_SPECIFIED,
                embedding=self.embedding.mapItem(i.item)
            ),
            feedback=feedback
        )


class MapVectorizedUser(mapper.MapperBase[Emb_pb2, VectorizedUser]):
    def __init__(self, embedding: mapper.MapperBase[Emb_pb2, Embedding]):
        super().__init__()
        self.embedding = embedding

    def mapItem(self, i):

        return VectorizedUser(
            user_id=uuid.UUID(int=0),
            embedding=self.embedding.mapItem(i),
            sex=Gender.NOT_SPECIFIED,
        )
