import os

import pytest
from fastapi.testclient import TestClient

from src.entrypoints.fastapi_app import app, get_uow
from src.service_layer import csv_uow

client = TestClient(app)


@pytest.fixture
def csv_uow_fixture():
    test_csv = "data/test_products.csv"
    if os.path.exists(test_csv):
        os.remove(test_csv)
    uow = csv_uow.CsvUnitOfWork(test_csv)
    yield uow
    if os.path.exists(test_csv):
        os.remove(test_csv)


@pytest.fixture(autouse=True)
def auto_clear_dependency_overrides():
    yield
    app.dependency_overrides = {}


def test_add_product(csv_uow_fixture):
    app.dependency_overrides[get_uow] = lambda: csv_uow_fixture
    response = client.post(
        "/products/",
        json={
            "sku": "PROD123",
            "name": "Test Product",
            "description": "This is a test product.",
            "price": 99.99,
            "brand": "TestBrand",
            "category": "TestCategory",
            "stock": 100,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "PROD123"
    assert data["name"] == "Test Product"

    # Verify the product was actually added
    response = client.get("/products/PROD123")
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "PROD123"


def test_add_product_invalid_sku(csv_uow_fixture):
    app.dependency_overrides[get_uow] = lambda: csv_uow_fixture
    # Add a product first
    client.post(
        "/products/",
        json={
            "sku": "PROD123",
            "name": "Test Product",
            "description": "This is a test product.",
            "price": 99.99,
            "brand": "TestBrand",
            "category": "TestCategory",
            "stock": 100,
        },
    )
    # Try to add it again
    response = client.post(
        "/products/",
        json={
            "sku": "PROD123",
            "name": "Another Test Product",
            "description": "This is another test product.",
            "price": 199.99,
            "brand": "AnotherTestBrand",
            "category": "AnotherTestCategory",
            "stock": 200,
        },
    )
    assert response.status_code == 400
    assert "Invalid sku PROD123" in response.json()["detail"]


def test_get_product_not_found(csv_uow_fixture):
    app.dependency_overrides[get_uow] = lambda: csv_uow_fixture
    response = client.get("/products/NONEXISTENT")
    assert response.status_code == 404
    assert "Product with SKU NONEXISTENT not found" in response.json()["detail"]


def test_list_products(csv_uow_fixture):
    app.dependency_overrides[get_uow] = lambda: csv_uow_fixture
    client.post(
        "/products/",
        json={
            "sku": "PROD1",
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.0,
            "brand": "Brand1",
            "category": "Category1",
            "stock": 10,
        },
    )
    client.post(
        "/products/",
        json={
            "sku": "PROD2",
            "name": "Product 2",
            "description": "Description 2",
            "price": 20.0,
            "brand": "Brand2",
            "category": "Category2",
            "stock": 20,
        },
    )

    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["sku"] == "PROD1"
    assert data[1]["sku"] == "PROD2"
