from dataclasses import dataclass


@dataclass
class Embedding:
    """Represents an embedding vector"""
    data: list[float]
