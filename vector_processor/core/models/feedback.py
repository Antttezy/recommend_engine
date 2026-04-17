from dataclasses import dataclass
import enum

from .embedding import Embedding


class FeedbackType(enum.Enum):
    POSITIVE = 1
    NEGATIVE = 2


@dataclass
class Feedback:
    item: Embedding
    feedback: FeedbackType
