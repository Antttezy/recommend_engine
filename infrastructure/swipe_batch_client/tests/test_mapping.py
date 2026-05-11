import uuid

from core.models import Embedding, ItemFeedback, FeedbackType, VectorizedItem, Gender
from infrastructure.swipe_batch_client.models import BatchedItem, BatchedFeedback
from infrastructure.swipe_batch_client.mapping import (
    map_from_batched_feedback, map_to_batched_feedback
)

from infrastructure.swipe_batch_client.tests.fixtures import random_embedding


def test_map1(random_embedding):
    embedding = Embedding(data=random_embedding)

    model = ItemFeedback(
        item=VectorizedItem(item_id=uuid.uuid4(),
                            in_stock=True,
                            embedding_ready=True,
                            sex=Gender.MALE,
                            embedding=embedding),
        feedback=FeedbackType.POSITIVE
    )

    mapped = map_to_batched_feedback(model)
    restored = map_from_batched_feedback(mapped)

    assert restored.item.item_id == model.item.item_id
    assert restored.item.in_stock == model.item.in_stock
    assert restored.item.embedding_ready == model.item.embedding_ready
    assert restored.item.sex == model.item.sex
    assert restored.item.embedding == model.item.embedding
    assert restored.feedback == model.feedback


def test_map_from_batched(random_embedding):
    batched = BatchedFeedback(
        item=BatchedItem(itemId=uuid.uuid4(),
                         inStock=True,
                         embeddingReady=True,
                         sex='FEMALE',
                         embedding=random_embedding),
        feedback='NEGATIVE'
    )

    mapped = map_from_batched_feedback(batched)
    restored = map_to_batched_feedback(mapped)

    assert restored.item.item_id == batched.item.item_id
    assert restored.item.in_stock == batched.item.in_stock
    assert restored.item.embedding_ready == batched.item.embedding_ready
    assert restored.item.sex == batched.item.sex
    assert restored.item.embedding == batched.item.embedding
    assert restored.feedback == batched.feedback
