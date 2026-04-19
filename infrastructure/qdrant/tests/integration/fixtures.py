import os
import pytest
import random

from qdrant_client import AsyncQdrantClient
from core.models import Embedding
from core.const import EMBEDDING_LENGTH


@pytest.fixture
def qdrant_client():
    url = os.getenv("QDRANT_URL")
    return AsyncQdrantClient(url)


@pytest.fixture
def skip_not_integration():
    run_integration = os.getenv("RUN_INTEGRATION", None)

    if not run_integration:
        pytest.skip("--run-integration not set")


@pytest.fixture
def random_embedding() -> Embedding:
    data = [random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)]
    return Embedding(data)
