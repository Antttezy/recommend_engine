import io
import uuid
import json

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import ItemInfo
from core.models import ItemUpdate, Gender, Photo
from vector_processor.core import ports, errors


class MapItemInfoItemUpdate(ports.Mapper[ItemInfo, ItemUpdate]):
    def mapItem(self, i):
        attrs_dict = json.loads(i.attributes_json)

        try:
            photos = [
                Photo(img=Image.open(io.BytesIO(x)))
                for x in i.photos]
        except:
            raise errors.MappingError("item_photo")

        return ItemUpdate(
            item_id=uuid.UUID(int=0),
            name=i.name,
            price=i.price,
            description=i.description,
            attributes=attrs_dict,
            photos=photos,
            sex=Gender.NOT_SPECIFIED
        )
