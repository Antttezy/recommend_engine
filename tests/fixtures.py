import random

import pytest
from PIL import Image

from core.const import EMBEDDING_LENGTH
from core.models import Embedding


@pytest.fixture
def image():
    return Image.new("RGB", (1, 1), 'blue')


@pytest.fixture
def random_embedding():
    return Embedding([random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)])


@pytest.fixture
def zero_embedding():
    return Embedding([0.0] * EMBEDDING_LENGTH)
