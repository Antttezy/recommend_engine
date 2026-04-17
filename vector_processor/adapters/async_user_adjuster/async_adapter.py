from vector_processor.core import ports


class UserAdjusterAsyncAdapter(ports.AsyncUserAdjuster):
    def __init__(self, user_adjuster: ports.UserAdjuster):
        super().__init__()
        self.__user_adjuster = user_adjuster

    async def adjust_user_embedding(self, user, feedbacks):
        return self.__user_adjuster.adjust_user_embedding(user, feedbacks)
