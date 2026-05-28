import random

import pytest

from core.const import EMBEDDING_LENGTH
from core.models import Embedding


def test_embedding_iszero():
    zero_data = [0.0] * 512
    data = [random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)]

    embedding = Embedding(data)
    zero_embedding = Embedding(zero_data)

    assert not embedding.is_zero()
    assert zero_embedding.is_zero()


def test_embedding_typecheck():
    try:
        # Not list
        Embedding(0)
    except TypeError:
        pass
    else:
        pytest.fail("expected to raise TypeError")

    try:
        # Wrong length list
        Embedding([0.0, 0.0, 0.0])
    except ValueError:
        pass
    else:
        pytest.fail("expected to raise ValueError")

    try:
        # Wrong element type
        Embedding(['1'] * 512)
    except TypeError:
        pass
    else:
        pytest.fail("expected to raise TypeError")
