from dataclasses import dataclass
from uuid import UUID


@dataclass
class CachedItem:
    item_id: UUID
