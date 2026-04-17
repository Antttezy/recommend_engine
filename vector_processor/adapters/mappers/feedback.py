from api.grpc.vector_processor.vector_processor_pb2 import AdjustUserRequest, Embedding
from vector_processor.core import ports, models


class MapFeedback(ports.Mapper[AdjustUserRequest.Feedback, models.Feedback]):
    def __init__(self, embedding: ports.Mapper[Embedding, models.Embedding]):
        super().__init__()
        self.embedding = embedding

    def mapItem(self, i):
        feedback: models.FeedbackType

        if i.feedback == AdjustUserRequest.FeedbackType.POSITIVE:
            feedback = models.FeedbackType.POSITIVE
        else:
            feedback = models.FeedbackType.NEGATIVE

        return models.Feedback(
            item=self.embedding.mapItem(i.item),
            feedback=feedback
        )
