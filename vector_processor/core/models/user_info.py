from dataclasses import dataclass
import datetime
from PIL.Image import Image


@dataclass
class UserInfo:
    first_name: str
    second_name: str
    avatar: Image
    country: str
    city: str
    birthday: datetime.datetime
