import uuid

from core import models, ports


class VectorizedUserRepoMock(ports.VectorizedUserRepo):
    def __init__(self):
        self.users = dict[uuid.UUID, models.VectorizedUser]()

    async def add(self, vectorized_user):
        assert self.users.get(vectorized_user.user_id) is None
        self.users[vectorized_user.user_id] = vectorized_user

    async def update(self, vectorized_user):
        assert self.users.get(vectorized_user.user_id) is not None
        self.users[vectorized_user.user_id] = vectorized_user

    async def get_by_id(self, user_id):
        return self.users.get(user_id)
