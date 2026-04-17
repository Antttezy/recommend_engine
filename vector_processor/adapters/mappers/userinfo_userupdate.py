import io
import uuid

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import UserInfo
from core.models import UserUpdate, Gender
from vector_processor.core import ports, errors


class MapUserInfoUserUpdate(ports.Mapper[UserInfo, UserUpdate]):
    def mapItem(self, i):

        try:
            avatar = Image.open(io.BytesIO(i.avatar))
        except:
            raise errors.MappingError("user_photo")

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
