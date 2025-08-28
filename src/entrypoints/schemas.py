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


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
