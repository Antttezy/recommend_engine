import asyncio
import logging
import os

from vector_processor import config


async def main():
    from transformers import CLIPModel, CLIPProcessor

    # Config and logging
    settings = config.load_config()
    logging.basicConfig(level=logging.getLevelNamesMapping()[settings.LOG_LEVEL])

    # CLIP device
    ml_device = "cpu"

    # Download models to cache
    CLIPModel.from_pretrained(settings.CLIP_MODEL).to(ml_device)
    CLIPProcessor.from_pretrained(settings.CLIP_PROCESSOR)


if __name__ == "__main__":
    # Unset variables triggering strict offline mode
    os.environ.pop("TRANSFORMERS_OFFLINE", None)
    os.environ.pop("HF_DATASETS_OFFLINE", None)
    asyncio.run(main())
