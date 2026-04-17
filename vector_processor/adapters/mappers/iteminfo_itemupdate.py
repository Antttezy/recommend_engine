import io
import json

from PIL import Image

from api.grpc.vector_processor.vector_processor_pb2 import ItemInfo
from vector_processor.core import ports, errors, models


class MapItemInfoItemUpdate(ports.Mapper[ItemInfo, models.ItemInfo]):
    def mapItem(self, i):
        attrs_dict = json.loads(i.attributes_json)

        try:
            photos = [
                Image.open(io.BytesIO(x))
                for x in i.photos]
        except:
            raise errors.MappingError("item_photo")

        return models.ItemInfo(
            name=i.name,
            price=i.price,
            description=i.description,
            attributes=attrs_dict,
            photos=photos
        )
