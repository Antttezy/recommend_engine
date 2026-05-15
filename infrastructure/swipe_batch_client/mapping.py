from core import models

from .models import BatchedFeedback, BatchedItem


def map_to_batched_feedback(feedback: models.ItemFeedback) -> BatchedFeedback:
    embedding = feedback.item.embedding.data
    sex = feedback.item.sex.name
    fbtype = feedback.feedback.name

    return BatchedFeedback(
        item=BatchedItem(itemId=feedback.item.item_id,
                         inStock=feedback.item.in_stock,
                         embeddingReady=feedback.item.embedding_ready,
                         sex=sex,
                         embedding=embedding),
        feedback=fbtype
    )


def map_from_batched_feedback(feedback: BatchedFeedback) -> models.ItemFeedback:
    embedding = models.Embedding(data=feedback.item.embedding)
    sex = models.Gender[feedback.item.sex]
    fbtype = models.FeedbackType[feedback.feedback]

    return models.ItemFeedback(
        item=models.VectorizedItem(item_id=feedback.item.item_id,
                                   in_stock=feedback.item.in_stock,
                                   embedding_ready=feedback.item.embedding_ready,
                                   sex=sex,
                                   embedding=embedding),
        feedback=fbtype
    )
