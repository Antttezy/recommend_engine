import datetime
import os
import uuid
import pytest

from PIL import Image
from grpc.aio import insecure_channel

from core import models

from .factory import new_grpc_vector_processor_client
from .errors import VectorizationError


@pytest.fixture
def image():
    return Image.new("RGB", (1, 1), 'blue')


@pytest.fixture
def skip_not_integration():
    run_integration = os.getenv("RUN_INTEGRATION", None)

    if not run_integration:
        pytest.skip("--run-integration not set")


@pytest.mark.asyncio
async def test_get_item_embedding(skip_not_integration, image):
    url = os.getenv("VECTOR_PROCESSOR_ENDPOINT")
    async with insecure_channel(url) as channel:
        client = new_grpc_vector_processor_client(channel)
        update = models.ItemUpdate(
            item_id=uuid.uuid4(),
            name="T-shirt",
            price=150.0,
            description='Lorem Ipsum',
            attributes={"a": 1, "b": 2},
            photos=[models.Photo(img=image)],
            sex=models.Gender.FEMALE
        )

        embedding = await client.get_item_embedding(update)
        assert embedding is not None
        assert not embedding.is_zero()


@pytest.mark.asyncio
async def test_get_item_nophoto(skip_not_integration):
    url = os.getenv("VECTOR_PROCESSOR_ENDPOINT")
    async with insecure_channel(url) as channel:
        client = new_grpc_vector_processor_client(channel)
        update = models.ItemUpdate(
            item_id=uuid.uuid4(),
            name="T-shirt",
            price=150.0,
            description='Lorem Ipsum',
            attributes={"a": 1, "b": 2},
            photos=[],
            sex=models.Gender.FEMALE
        )

        try:
            await client.get_item_embedding(update)
        except VectorizationError:
            pass
        else:
            pytest.fail("Vector processor client should not accept items without photos")


@pytest.mark.asyncio
async def test_get_user_embedding(skip_not_integration, image):
    url = os.getenv("VECTOR_PROCESSOR_ENDPOINT")
    async with insecure_channel(url) as channel:
        client = new_grpc_vector_processor_client(channel)
        update = models.UserUpdate(
            user_id=uuid.uuid4(),
            first_name="John",
            second_name="Smith",
            avatar=image,
            country='RU',
            city='Moscow',
            birthday=datetime.datetime(2000, 1, 1),
            sex=models.Gender.MALE
        )

        embedding = await client.get_user_embedding(update)
        assert embedding is not None


@pytest.mark.asyncio
async def test_adjust_user_embedding(skip_not_integration):
    url = os.getenv("VECTOR_PROCESSOR_ENDPOINT")
    async with insecure_channel(url) as channel:
        client = new_grpc_vector_processor_client(channel)
        user_emb = models.Embedding([0.0] * 512)
        item_emb = models.Embedding([1.0 if i == 1 else 0.0 for i in range(512)])
        user = models.VectorizedUser(uuid.uuid4(), models.Gender.MALE, user_emb)
        feedback = models.ItemFeedback(
            models.VectorizedItem(uuid.uuid4(), True, True, models.Gender.NOT_SPECIFIED, item_emb),
            # Negative feedback => we expect moving away from it
            models.FeedbackType.NEGATIVE
        )

        new_embedding = await client.adjust_user_embedding(user, [feedback])
        assert new_embedding is not None
        assert not new_embedding.is_zero()

        # Check if new embedding is opposite of item embedding
        assert all([a == pytest.approx(-b) for a, b in zip(new_embedding.data, item_emb.data)])
