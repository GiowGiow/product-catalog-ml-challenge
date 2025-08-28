from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    brand: str
    category: str
    stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    created_at: date
    updated_at: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
