from dataclasses import dataclass


@dataclass
class Embedding:
    EMBEDDING_LENGTH = 512
    """Represents an embedding vector"""
    data: list[float]

    def __post_init__(self):
        if not isinstance(self.data, list):
            raise TypeError("Embedding.data must be a list")

        if len(self.data) != Embedding.EMBEDDING_LENGTH:
            raise ValueError(
                f"Embeddings must be {Embedding.EMBEDDING_LENGTH}-dimentional, got {len(self.data)}"
            )

        if not all(isinstance(x, (float, int)) for x in self.data):
            raise TypeError("Embedding must contain only numeric values")
