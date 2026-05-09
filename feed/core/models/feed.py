from dataclasses import dataclass
from uuid import UUID


@dataclass
class FeedItem:
    item_id: UUID
