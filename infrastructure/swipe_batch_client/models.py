from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


EMBEDDING_LENGTH = 512


class BatchedItem(BaseModel):
    item_id: UUID = Field(alias='itemId')
    in_stock: bool = Field(alias='inStock')
    embedding_ready: bool = Field(alias='embeddingReady')
    sex: Literal['NOT_SPECIFIED', 'MALE', 'FEMALE']
    embedding: list[float] = Field(min_length=EMBEDDING_LENGTH, max_length=EMBEDDING_LENGTH)


class BatchedFeedback(BaseModel):
    item: BatchedItem
    feedback: Literal['POSITIVE', 'NEGATIVE']
