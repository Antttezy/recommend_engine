from dataclasses import dataclass
from enum import Enum

from .vectorized_item import VectorizedItem


class FeedbackType(Enum):
    POSITIVE = 1
    NEGATIVE = 2


@dataclass
class ItemFeedback:
    item: VectorizedItem
    feedback: FeedbackType
