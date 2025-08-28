from src.adapters.repository import AbstractRepository
from src.domain import model


class FakeRepository(AbstractRepository):
    def __init__(self, products):
        self._products = set(products)

    def add(self, product: model.Product):
        self._products.add(product)

    def get(self, sku: str) -> model.Product:
        return next(p for p in self._products if p.sku == sku)

    def list(self) -> list[model.Product]:
        return list(self._products)
