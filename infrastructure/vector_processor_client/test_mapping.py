import datetime
import random
import uuid

import pytest
from PIL import Image
from api.grpc.vector_processor.vector_processor_pb2 import AdjustUserRequest, Embedding as Emb_pb2
from core.models import UserUpdate, Gender, ItemUpdate, Photo, VectorizedUser, VectorizedItem
from core.models import Embedding, ItemFeedback, FeedbackType
from core.const import EMBEDDING_LENGTH
from . import mapping


@pytest.fixture
def image():
    return Image.new("RGB", (1, 1), 'blue')


@pytest.fixture
def random_data():
    return [random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)]


def test_map_userupdate(image):
    user = UserUpdate(
        user_id=uuid.uuid4(),
        first_name="John",
        second_name="Smith",
        avatar=image,
        country='GB',
        city='London',
        birthday=datetime.datetime.now(),
        sex=Gender.MALE
    )

    info = mapping.map_userupdate(user)

    assert info.first_name == user.first_name
    assert info.second_name == user.second_name
    assert info.avatar is not None
    assert len(info.avatar) > 0
    assert info.country == user.country
    assert info.city == user.city
    assert info.birthday.ToDatetime() == user.birthday


def test_map_itemupdate(image):
    item = ItemUpdate(
        item_id=uuid.uuid4(),
        name="T-Shirt",
        price=1412.5,
        description="Nice",
        attributes={"a": 1, "b": 2},
        photos=[Photo(img=image)],
        sex=Gender.NOT_SPECIFIED
    )

    info = mapping.map_itemupdate(item)

    assert info.name == item.name
    assert info.price == item.price
    assert info.description == item.description
    assert info.attributes_json
    assert len(info.photos) == 1
    assert len(info.photos[0]) > 0


def test_map_vectorizeduser(random_data):
    user = VectorizedUser(
        user_id=uuid.uuid4(),
        sex=Gender.FEMALE,
        embedding=Embedding(random_data)
    )

    emb = mapping.map_vectorizeduser(user)

    assert emb.data == random_data


def test_map_feedback(random_data):
    feed = ItemFeedback(
        item=VectorizedItem(
            item_id=uuid.uuid4(),
            sex=Gender.MALE,
            embedding=Embedding(random_data),
            in_stock=True,
            embedding_ready=False
        ),
        feedback=FeedbackType.POSITIVE
    )

    mapped = mapping.map_feedback(feed)

    assert mapped.item.data == random_data
    assert mapped.feedback == AdjustUserRequest.FeedbackType.POSITIVE


def test_map_feedbacks(random_data):
    rand2 = [x for x in random_data]
    rand2[0] *= -1

    feeds = [
        ItemFeedback(
            item=VectorizedItem(
                item_id=uuid.uuid4(),
                sex=Gender.MALE,
                embedding=Embedding(random_data),
                in_stock=True,
                embedding_ready=True
            ),
            feedback=FeedbackType.POSITIVE
        ),
        ItemFeedback(
            item=VectorizedItem(
                item_id=uuid.uuid4(),
                sex=Gender.FEMALE,
                embedding=Embedding(rand2),
                in_stock=True,
                embedding_ready=False
            ),
            feedback=FeedbackType.NEGATIVE
        ),
    ]

    mapped = mapping.map_feedback_list(feeds)

    assert len(mapped) == 2
    assert mapped[0].item.data == random_data
    assert mapped[1].item.data == rand2

    assert mapped[0].feedback == AdjustUserRequest.FeedbackType.POSITIVE
    assert mapped[1].feedback == AdjustUserRequest.FeedbackType.NEGATIVE


def test_reverse_map_embedding(random_data):
    embedding = Emb_pb2(data=random_data)
    mapped = mapping.reverse_map_embedding(embedding)
    assert mapped.data == random_data
