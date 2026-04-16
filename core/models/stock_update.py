from dataclasses import dataclass
import uuid

@dataclass
class StockUpdate:
    item_id: uuid.UUID
    amount: int
