import io
import uuid
import json

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import ItemInfo
from core.models import ItemUpdate, Gender, Photo
from vector_processor import mapper


class MapItemInfoItemUpdate(mapper.MapperBase[ItemInfo, ItemUpdate]):
    def mapItem(self, i):
        attrs_dict = json.loads(i.attributes_json)

        photos = [
            Photo(img=Image.open(io.BytesIO(x)))
            for x in i.photos]

        return ItemUpdate(
            item_id=uuid.UUID(int=0),
            name=i.name,
            price=i.price,
            description=i.description,
            attributes=attrs_dict,
            photos=photos,
            sex=Gender.NOT_SPECIFIED
        )
