import datetime
import io
import random

import pytest
from PIL import Image

from api.grpc.vector_processor import vector_processor_pb2
from vector_processor.core import models
from vector_processor.adapters import mappers


@pytest.fixture
def random_data():
    return [random.random() * 2 - 1 for _ in range(models.Embedding.EMBEDDING_LENGTH)]


@pytest.fixture
def image_bytes():
    with Image.new("RGB", (1, 1), 'blue') as img:
        with io.BytesIO() as bio:
            img.save(bio, 'png')
            bio.seek(0)
            return bio.read()


def test_map_embedding(random_data):
    mapper = mappers.MapProtoEmbeddingEmbedding()

    model_in = vector_processor_pb2.Embedding(data=random_data)
    model_out = mapper.mapItem(model_in)

    assert len(model_in.data) == len(model_out.data)
    assert all([a == b for a, b in zip(model_in.data, model_out.data)])


def test_map_embedding_response(random_data):
    mapper = mappers.MapEmbeddingProtoEmbedding()
    model_in = models.Embedding(data=random_data)
    model_out = mapper.mapItem(model_in)

    assert len(model_in.data) == len(model_out.data)
    assert all([a == b for a, b in zip(model_in.data, model_out.data)])


def test_map_iteminfo(image_bytes):
    model_in = vector_processor_pb2.ItemInfo(
        name="T-shirt",
        price=150.0,
        description='Lorem Ipsum',
        attributes_json='{"a":1,"b":2}',
        photos=[image_bytes]
    )

    mapper = mappers.MapItemInfoItemUpdate()
    model_out = mapper.mapItem(model_in)

    assert model_in.name == model_out.name
    assert model_in.price == model_out.price
    assert model_in.description == model_out.description

    assert len(model_in.photos) == len(model_out.photos)

    assert model_out.attributes['a'] == 1
    assert model_out.attributes['b'] == 2
    assert model_out.photos[0].getpixel((0, 0)) == (0, 0, 255)


def test_map_userinfo(image_bytes):
    model_in = vector_processor_pb2.UserInfo(
        first_name="John",
        second_name="Smith",
        avatar=image_bytes,
        country="GB",
        city="London",
        birthday=datetime.datetime(2000, 1, 1)
    )

    mapper = mappers.MapUserInfoUserUpdate()
    model_out = mapper.mapItem(model_in)

    assert model_in.first_name == model_out.first_name
    assert model_in.second_name == model_out.second_name
    assert model_in.country == model_out.country
    assert model_in.city == model_out.city

    date_in = model_in.birthday.ToDatetime()
    date_out = model_out.birthday
    assert date_in == date_out

    assert model_out.avatar.getpixel((0, 0)) == (0, 0, 255)


def test_map_feedback(random_data):
    model_in = vector_processor_pb2.AdjustUserRequest.Feedback(
        item=vector_processor_pb2.Embedding(data=random_data),
        feedback=vector_processor_pb2.AdjustUserRequest.FeedbackType.NEGATIVE
    )

    mapper = mappers.MapFeedback(mappers.MapProtoEmbeddingEmbedding())
    model_out = mapper.mapItem(model_in)

    assert len(model_in.item.data) == len(model_out.item.data)
    assert all([a == b for a, b in zip(model_in.item.data, model_out.item.data)])

    assert model_out.feedback == models.FeedbackType.NEGATIVE
