from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    price: int
    status: str
    created_at: datetime
