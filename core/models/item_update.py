from dataclasses import dataclass
import uuid

from PIL.Image import Image

from core.models import Gender


@dataclass
class Photo:
    img: Image


@dataclass
class ItemUpdate:
    item_id: uuid.UUID
    name: str
    price: float
    description: str
    attributes: dict
    photos: list[Photo]
    sex: Gender
