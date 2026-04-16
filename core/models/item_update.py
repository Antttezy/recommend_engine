from dataclasses import dataclass
import uuid

from core.models import Gender


@dataclass
class Photo:
    url: str


@dataclass
class ItemUpdate:
    item_id: uuid.UUID
    name: str
    price: float
    description: str
    attributes: dict
    photos: list[Photo]
    sex: Gender
