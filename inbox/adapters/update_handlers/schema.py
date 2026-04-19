import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ItemUpdateSchema(BaseModel):
    item_id: UUID = Field(alias="itemId")
    name: str
    price: float
    description: str
    attributes: dict = Field({})
    photos: list[str]
    sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"]


class StockUpdateSchema(BaseModel):
    item_id: UUID = Field(alias="itemId")
    amount: int


class UserUpdateSchema(BaseModel):
    user_id: UUID = Field(alias="userId")
    first_name: str = Field(alias='firstName')
    second_name: str = Field(alias='secondName')
    avatar: str
    country: str
    city: str
    birthday: datetime.datetime
    sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"]

    @field_validator('birthday', mode='before')
    @classmethod
    def parse_birthday(cls, value: str) -> datetime.datetime:
        if isinstance(value, str):
            date = datetime.datetime.strptime(value, "%d-%m-%Y")
            return datetime.datetime(date.year, date.month, date.day, tzinfo=datetime.UTC)

        return ValueError("incorrect birthday format")
