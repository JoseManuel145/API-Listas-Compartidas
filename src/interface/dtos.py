from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class SharedListCreate(BaseModel):
    name: str

class SharedListResponse(SharedListCreate):
    id: UUID
    created_at: datetime

    class config:
        from_atributes: True

class ProductCreate(BaseModel):
    list_id: UUID
    name: str
    quantity: int

class ProductResponse(ProductCreate):
    id: UUID
    list_id: UUID
    status: str
    created_at: datetime

    class config:
        from_atributes: True
