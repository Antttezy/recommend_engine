from dataclasses import dataclass
from PIL.Image import Image


@dataclass
class ItemInfo:
    name: str
    price: float
    description: str
    attributes: dict
    photos: list[Image]
