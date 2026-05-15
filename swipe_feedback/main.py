import logging

import uvicorn

from swipe_feedback import config
from swipe_feedback.rest import create_api


def main():
    settings = config.load_settings()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])

    api = create_api(settings)

    uvicorn.run(
        api,
        host='0.0.0.0',
        port=settings.HTTP_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
