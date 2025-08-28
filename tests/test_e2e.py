import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenario, then, when

from src.entrypoints.fastapi_app import app, get_uow
from src.service_layer.csv_uow import CsvUnitOfWork

# Constants
BASE_URL = "/products"


@pytest.fixture
def test_csv_file(tmp_path):
    """Create a temporary csv file for testing."""
    return tmp_path / "test_products.csv"


@pytest.fixture
def client(test_csv_file):
    """A TestClient that uses a temporary CSV file."""

    def override_get_uow():
        return CsvUnitOfWork(filepath=str(test_csv_file))

    app.dependency_overrides[get_uow] = override_get_uow
    yield TestClient(app)
    del app.dependency_overrides[get_uow]


@scenario(
    "features/product_retrieval.feature",
    "Retrieve an existing product's details successfully",
)
def test_retrieving_existing_product():
    pass


@scenario(
    "features/product_retrieval.feature", "Attempt to retrieve a non-existent product"
)
def test_retrieving_non_existent_product():
    pass


@scenario(
    "features/product_listing.feature", "List all products when multiple products exist"
)
def test_list_all_products():
    pass


@scenario(
    "features/product_listing.feature", "List all products when the catalog is empty"
)
def test_list_all_products_empty():
    pass


@scenario("features/product_management.feature", "Successfully add a new product")
def test_add_new_product():
    pass


@scenario(
    "features/product_management.feature",
    "Attempt to add a product with a duplicate SKU",
)
def test_add_duplicate_product():
    pass


@given("the system is running")
def system_is_running():
    """This step is a placeholder for readability in feature files."""
    pass


@given("the system has no products")
def clear_products(test_csv_file):
    """Ensure the temporary CSV file is empty."""
    if test_csv_file.exists():
        test_csv_file.unlink()


@given(
    parsers.parse("the system has the following products:"),
    target_fixture="products_context",
)
def system_has_products(client, datatable):
    products = []
    headers = [h.lower() for h in datatable[0]]
    for row_values in datatable[1:]:
        row = dict(zip(headers, row_values))
        product = {
            "sku": row["sku"],
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "brand": row["brand"],
            "category": row["category"],
            "stock": int(row["stock"]),
        }
        client.post(BASE_URL, json=product)
        products.append(product)
    return {"products": products}


@given(parsers.parse('a product with sku "{sku}" exists'))
def product_with_sku_exists(client, sku):
    product_data = {
        "sku": sku,
        "name": "Existing Product",
        "description": "A product that already exists.",
        "price": 50.00,
        "brand": "ExistingBrand",
        "category": "ExistingCategory",
        "stock": 10,
    }
    # Ensure it doesn't fail if it already exists from another step
    client.post(BASE_URL, json=product_data)


@when(
    parsers.parse('I request the product details for sku "{sku}"'),
    target_fixture="response",
)
def request_product_details(client, sku):
    return client.get(f"{BASE_URL}/{sku}")


@when("I request the list of all products", target_fixture="response")
def request_list_of_all_products(client):
    return client.get(BASE_URL)


@when("I add a new product with the following details:", target_fixture="response")
def add_new_product_step(client, datatable):
    headers = [h.lower() for h in datatable[0]]
    row_values = datatable[1]
    row = dict(zip(headers, row_values))
    product_data = {
        "sku": row["sku"].strip('"'),
        "name": row["name"].strip('"'),
        "description": row["description"].strip('"'),
        "price": float(row["price"]),
        "brand": row["brand"].strip('"'),
        "category": row["category"].strip('"'),
        "stock": int(row["stock"]),
    }
    return client.post(BASE_URL, json=product_data)


@when(
    parsers.parse('I try to add a new product with sku "{sku}"'),
    target_fixture="response",
)
def add_duplicate_product_step(client, sku):
    product_data = {
        "sku": sku,
        "name": "Duplicate Product",
        "description": "This is a duplicate product.",
        "price": 25.00,
        "brand": "DuplicateBrand",
        "category": "DuplicateCategory",
        "stock": 5,
    }
    return client.post(BASE_URL, json=product_data)


@then(parsers.parse("the response status code should be {status_code:d}"))
def response_status_code(response, status_code):
    assert response.status_code == status_code


@then(parsers.parse('the response should contain the details for the product "{sku}"'))
def response_contains_product_details(response, sku, products_context):
    expected_product = next(
        (p for p in products_context["products"] if p["sku"] == sku), None
    )
    assert expected_product is not None, f"Product with SKU {sku} not found in context."
    response_data = response.json()
    assert response_data["sku"] == expected_product["sku"]
    assert response_data["name"] == expected_product["name"]
    assert response_data["price"] == expected_product["price"]


@then(parsers.parse('the response should contain an error message "{message}"'))
def response_contains_error_message(response, message):
    assert message in response.json()["detail"]


@then(parsers.parse("the response should contain a list of {count:d} products"))
def response_contains_list_of_products(response, count):
    assert isinstance(response.json(), list)
    assert len(response.json()) == count


@then("the response should contain an empty list")
def response_contains_empty_list(response):
    assert response.json() == []


@then(parsers.parse('the product "{sku}" should be available in the system'))
def product_should_be_available(client, sku):
    response = client.get(f"{BASE_URL}/{sku.strip('"')}")
    assert response.status_code == 200
    assert response.json()["sku"] == sku.strip('"')
