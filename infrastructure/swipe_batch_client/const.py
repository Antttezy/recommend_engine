from uuid import UUID


SWIPE_BATCH_KEY = 'user/{id}/feedback_batch'


def get_swipe_batch_key(user_id: UUID):
    return SWIPE_BATCH_KEY.format(id=user_id)
