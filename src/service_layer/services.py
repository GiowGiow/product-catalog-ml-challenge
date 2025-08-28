from datetime import date

from src.domain import model
from src.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


class ProductNotFound(Exception):
    pass


def add_product(
    sku: str,
    name: str,
    description: str,
    price: float,
    brand: str,
    category: str,
    stock: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> model.Product:
    with uow:
        if uow.products.get(sku):
            raise InvalidSku(f"Invalid sku {sku}")
        product = model.Product(
            sku,
            name,
            description,
            price,
            brand,
            category,
            stock,
            created_at=date.today(),
        )
        uow.products.add(product)
        uow.commit()
        return product


def get_product(sku: str, uow: unit_of_work.AbstractUnitOfWork) -> model.Product:
    with uow:
        product = uow.products.get(sku)
        if not product:
            raise ProductNotFound(f"Product with SKU {sku} not found")
        return product


def list_products(uow: unit_of_work.AbstractUnitOfWork) -> list[model.Product]:
    with uow:
        return uow.products.list()
