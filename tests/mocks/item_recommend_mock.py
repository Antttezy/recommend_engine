import random
from uuid import uuid4

import pytest

from core import const, ports
from core.models import Embedding, Gender, VectorizedItem


class ItemRecommendMock(ports.ItemRecommend):
    def __init__(self):
        self.item_pool = [
            VectorizedItem(uuid4(), True, True, Gender.MALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.MALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.MALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.MALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.MALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.FEMALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.FEMALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.FEMALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.FEMALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.FEMALE, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.NOT_SPECIFIED, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.NOT_SPECIFIED, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.NOT_SPECIFIED, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.NOT_SPECIFIED, self.__rand_embedding()),
            VectorizedItem(uuid4(), True, True, Gender.NOT_SPECIFIED, self.__rand_embedding()),
        ]

    async def get_recommended(self, user, limit):
        pool = list(filter(
            lambda i: i.sex == Gender.NOT_SPECIFIED or i.sex == user.sex,
            self.item_pool
        ))

        lim = min(len(pool), limit)
        return random.sample(pool, lim)

    def __rand_embedding(self):
        return Embedding([random.random() * 2 - 1 for _ in range(const.EMBEDDING_LENGTH)])


class FailingItemRecommendMock(ports.ItemRecommend):
    async def get_recommended(self, user, limit):
        pytest.fail("This method must not be called")
