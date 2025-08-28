from datetime import date

import pytest

from src.adapters import repository
from src.domain import model
from src.service_layer import services, unit_of_work


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.products = repository.InMemoryRepository(set())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_product():
    uow = FakeUnitOfWork()
    services.add_product(
        "SKU123",
        "Test Product",
        "This is a test product.",
        99.99,
        "Test Brand",
        "Test Category",
        100,
        uow,
    )
    assert uow.products.get("SKU123") is not None
    assert uow.committed


def test_add_product_invalid_sku():
    uow = FakeUnitOfWork()
    product = model.Product(
        "SKU123",
        "Test Product",
        "This is a test product.",
        99.99,
        "Test Brand",
        "Test Category",
        100,
        date.today(),
    )
    uow.products.add(product)
    with pytest.raises(services.InvalidSku, match="Invalid sku SKU123"):
        services.add_product(
            "SKU123",
            "Test Product",
            "This is a test product.",
            99.99,
            "Test Brand",
            "Test Category",
            100,
            uow,
        )


def test_get_product_by_sku():
    uow = FakeUnitOfWork()
    product = model.Product(
        "SKU123",
        "Test Product",
        "This is a test product.",
        99.99,
        "Test Brand",
        "Test Category",
        100,
        date.today(),
    )
    uow.products.add(product)
    assert services.get_product("SKU123", uow) == product


def test_get_product_not_found():
    uow = FakeUnitOfWork()
    with pytest.raises(
        services.ProductNotFound, match="Product with SKU SKU123 not found"
    ):
        services.get_product("SKU123", uow)


def test_list_products():
    uow = FakeUnitOfWork()
    product1 = model.Product(
        "SKU123",
        "Test Product 1",
        "This is test product 1.",
        99.99,
        "Test Brand",
        "Test Category",
        100,
        date.today(),
    )
    product2 = model.Product(
        "SKU456",
        "Test Product 2",
        "This is test product 2.",
        199.99,
        "Test Brand",
        "Test Category",
        200,
        date.today(),
    )
    uow.products.add(product1)
    uow.products.add(product2)
    assert services.list_products(uow) == sorted(
        [product1, product2], key=lambda p: p.sku
    )
