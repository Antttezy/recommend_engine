from fastapi import Depends

from swipe_feedback.config import Settings
from .config import get_config


def feedback_batch(config: Settings = Depends(get_config)):
    return {'zero': config.FEEDBACK_BATCH_ZERO, 'default': config.FEEDBACK_BATCH_DEFAULT}
