from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.domain.enums import ProductStatus

@dataclass
class Product:
    id: UUID
    list_id: UUID
    name: str
    quantity: int
    status: ProductStatus
    created_at: datetime

@dataclass
class SharedList:
    id: UUID
    name: str
    created_at: datetime