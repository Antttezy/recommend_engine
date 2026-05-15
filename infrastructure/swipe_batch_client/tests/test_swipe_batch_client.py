import uuid
import pytest

from core.models import Embedding, ItemFeedback, FeedbackType, VectorizedItem, Gender
from infrastructure.swipe_batch_client.client import SwipeBatchClient
from infrastructure.swipe_batch_client.const import get_swipe_batch_key

from infrastructure.swipe_batch_client.tests.fixtures import (
    random_embedding, valkey_client, skip_not_integration)


@pytest.mark.asyncio
async def test_swipe_batch_client(skip_not_integration, valkey_client, random_embedding):
    user_id = uuid.uuid4()

    try:
        client = SwipeBatchClient(valkey_client)

        models = [
            ItemFeedback(
                item=VectorizedItem(item_id=uuid.uuid4(),
                                    in_stock=True,
                                    embedding_ready=True,
                                    sex=Gender.MALE,
                                    embedding=Embedding(data=random_embedding)),
                feedback=FeedbackType.POSITIVE
            ),
            ItemFeedback(
                item=VectorizedItem(item_id=uuid.uuid4(),
                                    in_stock=True,
                                    embedding_ready=True,
                                    sex=Gender.FEMALE,
                                    embedding=Embedding(data=random_embedding)),
                feedback=FeedbackType.NEGATIVE
            )
        ]

        assert await client.get_feedback_count(user_id) == 0
        batch = await client.get_feedback_items(user_id)
        assert len(batch) == 0

        await client.push_feedback(user_id, models[0])
        assert await client.get_feedback_count(user_id) == 1
        await client.push_feedback(user_id, models[1])
        assert await client.get_feedback_count(user_id) == 2
        assert await client.get_feedback_count(uuid.UUID(int=0)) == 0

        batch = await client.get_feedback_items(user_id)
        assert len(batch) == len(models) == 2
        batch = list(reversed(batch))

        for i in range(len(batch)):
            assert batch[i].item.item_id == models[i].item.item_id
            assert batch[i].item.in_stock == models[i].item.in_stock
            assert batch[i].item.embedding_ready == models[i].item.embedding_ready
            assert batch[i].item.sex == models[i].item.sex
            assert batch[i].item.embedding == models[i].item.embedding
            assert batch[i].feedback == models[i].feedback

        await client.clear_feedback(user_id)
        assert await client.get_feedback_count(user_id) == 0
    finally:
        key = get_swipe_batch_key(user_id)
        await valkey_client.delete(key)
