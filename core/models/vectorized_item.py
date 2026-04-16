from dataclasses import dataclass
import uuid

from .gender import Gender
from .embedding import Embedding


@dataclass
class VectorizedItem:
    item_id: uuid.UUID
    in_stock: bool
    sex: Gender
    embedding: Embedding
