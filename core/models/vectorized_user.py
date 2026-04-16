from dataclasses import dataclass
import uuid

from core.models import Gender, Embedding


@dataclass
class VectorizedUser:
    user_id: uuid.UUID
    sex: Gender
    embedding: Embedding
