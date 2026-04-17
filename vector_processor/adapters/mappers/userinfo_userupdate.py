import io

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import UserInfo
from vector_processor.core import ports, errors, models


class MapUserInfoUserUpdate(ports.Mapper[UserInfo, models.UserInfo]):
    def mapItem(self, i):

        try:
            avatar = Image.open(io.BytesIO(i.avatar))
        except:
            raise errors.MappingError("user_photo")

        return models.UserInfo(
            first_name=i.first_name,
            second_name=i.second_name,
            avatar=avatar,
            country=i.country,
            city=i.city,
            birthday=i.birthday.ToDatetime(),
        )
