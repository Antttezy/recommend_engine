from dataclasses import dataclass
import uuid

from core.models import Gender, Embedding


@dataclass
class VectorizedItem:
    item_id: uuid.UUID
    in_stock: bool
    sex: Gender
    embedding: Embedding
