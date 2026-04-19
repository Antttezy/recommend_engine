import io

from httpx import AsyncClient
from PIL import Image

from core import models
from inbox.core.errors import PayloadParseError

from .schema import ItemUpdateSchema, StockUpdateSchema, UserUpdateSchema


async def parse_item_update(data: bytes) -> models.ItemUpdate:
    try:
        schema = ItemUpdateSchema.model_validate_json(data)
    except Exception as e:
        raise PayloadParseError(*e.args)

    if schema.sex == "MALE":
        s = models.Gender.MALE
    elif schema.sex == "FEMALE":
        s = models.Gender.FEMALE
    else:
        s = models.Gender.NOT_SPECIFIED

    photos = []

    async with AsyncClient() as client:
        for url in schema.photos:
            response = await client.get(url)
            data = response.read()

            img = Image.open(io.BytesIO(data))
            photo = models.Photo(img)
            photos.append(photo)

    return models.ItemUpdate(
        item_id=schema.item_id,
        name=schema.name,
        price=schema.price,
        description=schema.description,
        attributes=schema.attributes,
        photos=photos,
        sex=s
    )


async def parse_stock_update(data: bytes) -> models.StockUpdate:
    try:
        schema = StockUpdateSchema.model_validate_json(data)
    except Exception as e:
        raise PayloadParseError(*e.args)

    return models.StockUpdate(schema.item_id, schema.amount)


async def parse_user_update(data: bytes) -> models.UserUpdate:
    try:
        schema = UserUpdateSchema.model_validate_json(data)
    except Exception as e:
        raise PayloadParseError(*e.args)

    if schema.sex == "MALE":
        s = models.Gender.MALE
    elif schema.sex == "FEMALE":
        s = models.Gender.FEMALE
    else:
        s = models.Gender.NOT_SPECIFIED

    async with AsyncClient() as client:
        response = await client.get(schema.avatar)
        data = response.read()

        img = Image.open(io.BytesIO(data))
        return models.UserUpdate(
            user_id=schema.user_id,
            first_name=schema.first_name,
            second_name=schema.second_name,
            avatar=img,
            country=schema.country,
            city=schema.city,
            birthday=schema.birthday,
            sex=s
        )
