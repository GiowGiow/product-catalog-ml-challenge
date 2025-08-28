import csv
import os
from datetime import date

from src.adapters import repository
from src.domain import model


def test_repository_can_add_a_product():
    repo = repository.InMemoryRepository(set())
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
    repo.add(product)
    assert repo.get("SKU123") == product


def test_repository_can_retrieve_a_product():
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
    repo = repository.InMemoryRepository([product])
    assert repo.get("SKU123") == product


def test_repository_can_list_products():
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
    repo = repository.InMemoryRepository([product1, product2])
    assert repo.list() == sorted([product1, product2], key=lambda p: p.sku)


def test_csv_repository_can_load_products(tmpdir):
    filepath = os.path.join(tmpdir, "products.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "sku",
                "name",
                "description",
                "price",
                "brand",
                "category",
                "stock",
                "created_at",
                "updated_at",
            ]
        )
        writer.writerow(
            [
                "SKU123",
                "Test Product",
                "This is a test product.",
                "99.99",
                "Test Brand",
                "Test Category",
                "100",
                date.today().isoformat(),
                "",
            ]
        )

    repo = repository.CsvRepository(filepath)
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
    assert repo.get("SKU123") == product
