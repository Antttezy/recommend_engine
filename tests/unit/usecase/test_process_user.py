import datetime
import uuid

import pytest

from core import const, models
from inbox.usecase import ProcessUserUsecase
from tests.mocks import VectorProcessorMock, VectorizedUserRepoMock
from tests.fixtures import image, random_embedding


@pytest.mark.asyncio
async def test_process_new_user(image):
    vector_processor = VectorProcessorMock()
    repo = VectorizedUserRepoMock()
    usecase = ProcessUserUsecase(vector_processor, repo)

    update = models.UserUpdate(
        user_id=uuid.uuid4(),
        first_name="John",
        second_name="Smith",
        avatar=image,
        country="US",
        city="New-York",
        birthday=datetime.datetime(1995, 1, 1),
        sex=models.Gender.MALE
    )

    await usecase.process_user(update)

    user = await repo.get_by_id(update.user_id)
    assert user is not None
    assert user.user_id == update.user_id
    assert user.sex == models.Gender.MALE
    assert user.embedding.is_zero()


@pytest.mark.asyncio
async def test_process_existing_user(image, random_embedding):
    vector_processor = VectorProcessorMock()
    repo = VectorizedUserRepoMock()
    usecase = ProcessUserUsecase(vector_processor, repo)

    user_id = uuid.uuid4()
    await repo.add(models.VectorizedUser(
        user_id=user_id,
        sex=models.Gender.NOT_SPECIFIED,
        embedding=random_embedding
    ))

    update = models.UserUpdate(
        user_id=user_id,
        first_name="John",
        second_name="Smith",
        avatar=image,
        country="US",
        city="New-York",
        birthday=datetime.datetime(1995, 1, 1),
        sex=models.Gender.MALE
    )

    await usecase.process_user(update)
    user = await repo.get_by_id(user_id)
    assert user is not None
    assert user.user_id == update.user_id
    assert user.sex == models.Gender.MALE
    assert user.embedding.is_zero()
