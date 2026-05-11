from fastapi import Depends

from feed.config import Settings
from .config import get_config


def feed_limits(config: Settings = Depends(get_config)):
    return {'zero': config.FEED_LIMIT_ZERO, 'default': config.FEED_LIMIT_DEFAULT}
