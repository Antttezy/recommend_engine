from dataclasses import dataclass
from enum import Enum

from core import models


class FeedbackType(Enum):
    POSITIVE = 1
    NEGATIVE = 2


@dataclass
class ItemFeedback:
    item: models.VectorizedItem
    feedback: FeedbackType
