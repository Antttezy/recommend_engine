import random
import os
import pytest
from valkey.asyncio import Valkey

from core.const import EMBEDDING_LENGTH


@pytest.fixture
def random_embedding() -> list[float]:
    data = [random.random() * 2 - 1 for _ in range(EMBEDDING_LENGTH)]
    return data


@pytest.fixture
def valkey_client():
    url = os.getenv("VALKEY_URL")
    return Valkey.from_url(url)


@pytest.fixture
def skip_not_integration():
    run_integration = os.getenv("RUN_INTEGRATION", None)

    if not run_integration:
        pytest.skip("--run-integration not set")
