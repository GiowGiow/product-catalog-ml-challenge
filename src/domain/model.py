from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Product:
    sku: str
    name: str
    description: str
    price: float
    brand: str
    category: str
    stock: int
    created_at: date
    updated_at: Optional[date] = None
