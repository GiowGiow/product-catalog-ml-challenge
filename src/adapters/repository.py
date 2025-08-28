import abc
import csv
from datetime import date
from typing import List, Optional

from src.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku: str) -> Optional[model.Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[model.Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, product: model.Product):
        raise NotImplementedError


class InMemoryRepository(AbstractRepository):
    def __init__(self, products):
        self._products = {p.sku: p for p in products}

    def add(self, product: model.Product):
        self._products[product.sku] = product

    def get(self, sku: str) -> Optional[model.Product]:
        return self._products.get(sku)

    def list(self) -> List[model.Product]:
        return sorted(list(self._products.values()), key=lambda p: p.sku)

    def remove(self, product: model.Product):
        if product.sku in self._products:
            del self._products[product.sku]


class CsvRepository(AbstractRepository):
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._products = self._load()

    def _load(self):
        products = {}
        try:
            with open(self._filepath, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product = model.Product(
                        sku=row["sku"],
                        name=row["name"],
                        description=row["description"],
                        price=float(row["price"]),
                        brand=row["brand"],
                        category=row["category"],
                        stock=int(row["stock"]),
                        created_at=date.fromisoformat(row["created_at"]),
                        updated_at=date.fromisoformat(row["updated_at"])
                        if row["updated_at"]
                        else None,
                    )
                    products[product.sku] = product
        except (FileNotFoundError, StopIteration):
            # Do not create the file here, let the UoW handle it.
            pass
        return products

    def add(self, product: model.Product):
        self._products[product.sku] = product

    def get(self, sku: str) -> Optional[model.Product]:
        return self._products.get(sku)

    def list(self) -> List[model.Product]:
        return sorted(list(self._products.values()), key=lambda p: p.sku)

    def remove(self, product: model.Product):
        if product.sku in self._products:
            del self._products[product.sku]
