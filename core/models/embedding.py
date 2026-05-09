from dataclasses import dataclass
from core.const import EMBEDDING_LENGTH


@dataclass
class Embedding:
    """Represents an embedding vector"""
    data: list[float]

    def __post_init__(self):
        if not isinstance(self.data, list):
            raise TypeError("Embedding.data must be a list")

        if len(self.data) != EMBEDDING_LENGTH:
            raise ValueError(
                f"Embeddings must be {EMBEDDING_LENGTH}-dimentional, got {len(self.data)}"
            )

        if not all(isinstance(x, (float, int)) for x in self.data):
            raise TypeError("Embedding must contain only numeric values")

    def is_zero(self):
        return all([x == 0 for x in self.data])
