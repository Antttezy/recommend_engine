from core import models, ports


class ProcessUserUsecase:
    def __init__(self,
                 vector_processor: ports.VectorProcessorClient,
                 repo: ports.VectorizedUserRepo):
        self.vector_processor = vector_processor
        self.repo = repo

    async def process_user(self, user: models.UserUpdate):
        embedding = await self.vector_processor.get_user_embedding(user)
        stored_user = await self.repo.get_by_id(user.user_id)

        if stored_user is not None:
            stored_user.embedding = embedding
            stored_user.sex = user.sex
            await self.repo.update(stored_user)

        else:
            stored_user = models.VectorizedUser(
                user_id=user.user_id,
                sex=user.sex,
                embedding=embedding
            )

            await self.repo.add(stored_user)
