from dataclasses import dataclass
import uuid

from .gender import Gender
from .embedding import Embedding


@dataclass
class VectorizedItem:
    item_id: uuid.UUID
    in_stock: bool
    embedding_ready: bool
    sex: Gender
    embedding: Embedding

    @property
    def ready(self):
        """Represents logical AND of all ready fields"""
        return self.embedding_ready
