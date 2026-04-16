from dataclasses import dataclass
import datetime
import uuid

from PIL.Image import Image

from core.models import Gender


@dataclass
class UserUpdate:
    user_id: uuid.UUID
    first_name: str
    second_name: str
    avatar: Image
    country: str
    city: str
    birthday: datetime.datetime
    sex: Gender
