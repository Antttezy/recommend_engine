import io
import uuid

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import UserInfo
from core.models import UserUpdate, Gender
from vector_processor import mapper


class MapUserInfoUserUpdate(mapper.MapperBase[UserInfo, UserUpdate]):
    def mapItem(self, i):
        avatar = Image.open(io.BytesIO(i.avatar))

        return UserUpdate(
            item_id=uuid.UUID(int=0),
            first_name=i.first_name,
            second_name=i.second_name,
            avatar=avatar,
            country=i.country,
            city=i.city,
            birthday=i.birthday.ToDatetime(),
            sex=Gender.NOT_SPECIFIED
        )
