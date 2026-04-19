import datetime
import uuid

import pytest

from core.models import Gender
from inbox.core.errors import PayloadParseError
from inbox.adapters.update_handlers.parsers import parse_item_update, parse_stock_update, parse_user_update


@pytest.mark.asyncio
async def test_parse_item_update():
    item = '{' \
        '"itemId": "786f44f4-89f2-4f9e-9ca8-35aeec97d1d4",' \
        '"name": "shirt",' \
        '"price": 42.5,' \
        '"description": "a nice shirt",' \
        '"attributes": {"a": 1, "b": 42, "c": 33},' \
        f'"photos": [],' \
        '"sex": "MALE"' \
        '}'

    parsed = await parse_item_update(item.encode())
    assert parsed.item_id == uuid.UUID("786f44f4-89f2-4f9e-9ca8-35aeec97d1d4")
    assert parsed.name == "shirt"
    assert parsed.price == 42.5
    assert parsed.description == "a nice shirt"
    assert parsed.attributes == {"a": 1, "b": 42, "c": 33}
    assert len(parsed.photos) == 0
    assert parsed.sex == Gender.MALE


@pytest.mark.asyncio
async def test_parse_incorrect_item_update():
    item = '{' \
        '"userId": "786f44f4-89f2-4f9e-9ca8-35aeec97d1d4",' \
        '"name": "shirt",' \
        '"price": 42.5,' \
        '"description": "a nice shirt",' \
        '"attributes": {"a": 1, "b": 42, "c": 33},' \
        f'"photos": [],' \
        '"sex": "MALE"' \
        '}'

    try:
        await parse_item_update(item.encode())
    except PayloadParseError:
        pass
    else:
        pytest.fail("expected to raise PayloadParseError")


@pytest.mark.asyncio
async def test_parse_stock_update():
    item = '{' \
        '"itemId": "786f44f4-89f2-4f9e-9ca8-35aeec97d1d4",' \
        '"amount": 43' \
        '}'

    parsed = await parse_stock_update(item.encode())
    assert parsed.item_id == uuid.UUID("786f44f4-89f2-4f9e-9ca8-35aeec97d1d4")
    assert parsed.amount == 43


@pytest.mark.asyncio
async def test_parse_incorrect_stock_update():
    item = '{' \
        '"itemId": "786f44f4-89f2-4f9e-9ca8-35aeec97d1d4",' \
        '"amount": "12.4"' \
        '}'

    try:
        stock = await parse_stock_update(item.encode())
        print(stock)
    except PayloadParseError:
        pass
    else:
        pytest.fail("expected to raise PayloadParseError")


@pytest.mark.asyncio
async def test_parse_user_update():
    user = '{' \
        '"userId": "56c91b61-779b-4b43-8d49-84cca3216a44",' \
        '"firstName": "John",' \
        '"secondName": "Smith",' \
        '"avatar": "https://www.google.com/favicon.ico",' \
        '"country": "GB",' \
        '"city": "London",' \
        '"birthday": "21-03-1989",' \
        '"sex": "MALE"' \
        '}'

    parsed = await parse_user_update(user.encode())
    assert parsed.user_id == uuid.UUID("56c91b61-779b-4b43-8d49-84cca3216a44")
    assert parsed.first_name == "John"
    assert parsed.second_name == "Smith"
    assert parsed.avatar is not None
    assert parsed.country == 'GB'
    assert parsed.city == 'London'
    assert parsed.birthday == datetime.datetime(1989, 3, 21, tzinfo=datetime.UTC)
    assert parsed.sex == Gender.MALE


@pytest.mark.asyncio
async def test_parse_incorrect_user_update():
    user = '{' \
        '"user_id": "56c91b61-779b-4b43-8d49-84cca3216a44",' \
        '"firstName": "John",' \
        '"secondName": "Smith",' \
        '"avatar": "https://www.google.com/favicon.ico",' \
        '"country": "GB",' \
        '"city": "London",' \
        '"birthday": "21-03-1989",' \
        '"sex": "MALE"' \
        '}'

    try:
        await parse_item_update(user.encode())
    except PayloadParseError:
        pass
    else:
        pytest.fail("expected to raise PayloadParseError")
