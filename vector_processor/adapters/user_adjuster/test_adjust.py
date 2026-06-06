import random
import pytest
import numpy

from vector_processor.core import models
from .fading_avg import FadingAvgUserAdjuster


@pytest.fixture
def random_data():
    return [random.random() * 2 - 1 for _ in range(models.Embedding.EMBEDDING_LENGTH)]


def test_empty_adjust(random_data):
    adjuster = FadingAvgUserAdjuster(0.1, 0.1, 0.05)

    # Normalize random data
    data = numpy.array(random_data)
    norm = numpy.linalg.norm(data)
    data = data / norm

    user = models.Embedding(data.tolist())
    new_user = adjuster.adjust_user_embedding(user, [])

    assert all([a == pytest.approx(b) for a, b in zip(user.data, new_user.data)])


def test_adjust(random_data):
    adjuster = FadingAvgUserAdjuster(0.1, 0.1, 0.05)

    # Normalize random data
    data = numpy.array(random_data)
    norm = numpy.linalg.norm(data)
    data = data / norm

    user = models.Embedding(data.tolist())

    feedbacks = [
        models.Feedback(models.Embedding(data.tolist()), models.FeedbackType.POSITIVE),
        models.Feedback(models.Embedding((-data).tolist()), models.FeedbackType.NEGATIVE),
    ]

    new_user = adjuster.adjust_user_embedding(user, feedbacks)

    assert new_user.data != user.data
