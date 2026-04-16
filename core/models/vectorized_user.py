from dataclasses import dataclass
import uuid

from .gender import Gender
from .embedding import Embedding


@dataclass
class VectorizedUser:
    user_id: uuid.UUID
    sex: Gender
    embedding: Embedding
