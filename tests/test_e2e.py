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


@scenario(
    "features/product_modification.feature", "Successfully edit an existing product"
)
def test_edit_existing_product():
    pass


@scenario(
    "features/product_modification.feature", "Attempt to edit a non-existent product"
)
def test_edit_non_existent_product():
    pass


@scenario(
    "features/product_modification.feature", "Successfully remove an existing product"
)
def test_remove_existing_product():
    pass


@scenario(
    "features/product_modification.feature", "Attempt to remove a non-existent product"
)
def test_remove_non_existent_product():
    pass


@scenario("features/authorization.feature", "Attempt to add a product without API key")
def test_add_product_without_api_key():
    pass


@scenario("features/authorization.feature", "Successfully add a product with API key")
def test_add_product_with_api_key():
    pass


@scenario("features/authorization.feature", "Attempt to edit a product without API key")
def test_edit_product_without_api_key():
    pass


@scenario("features/authorization.feature", "Successfully edit a product with API key")
def test_edit_product_with_api_key():
    pass


@scenario(
    "features/authorization.feature", "Attempt to remove a product without API key"
)
def test_remove_product_without_api_key():
    pass


@scenario(
    "features/authorization.feature", "Successfully remove a product with API key"
)
def test_remove_product_with_api_key():
    pass


# --- Given ---


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
def system_has_products(client, datatable, api_key_headers):
    products = []
    headers = [h.lower() for h in datatable[0]]
    for row_values in datatable[1:]:
        row = dict(zip(headers, row_values))
        product = {
            "sku": row["sku"].strip('"'),
            "name": row["name"].strip('"'),
            "description": row["description"].strip('"'),
            "price": float(row["price"]),
            "brand": row["brand"].strip('"'),
            "category": row["category"].strip('"'),
            "stock": int(row["stock"]),
        }
        client.post(BASE_URL, json=product, headers=api_key_headers)
        products.append(product)
    return {"products": products}


@given(parsers.parse('a product with sku "{sku}" exists'))
def product_with_sku_exists(client, sku, api_key_headers):
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
    client.post(BASE_URL, json=product_data, headers=api_key_headers)


@pytest.fixture(scope="session", autouse=True)
def api_key_headers():
    from src.entrypoints.fastapi_app import API_KEY

    return {"X-API-KEY": API_KEY}


@given("a product exists")
def product_exists(client, api_key_headers):
    client.post(
        BASE_URL,
        json={
            "sku": "PROD123",
            "name": "Test Product",
            "description": "A product for testing",
            "price": 10.0,
            "brand": "TestBrand",
            "category": "TestCategory",
            "stock": 10,
        },
        headers=api_key_headers,
    )


# --- When ---


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
def add_new_product_step(client, datatable, api_key_headers):
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
    return client.post(BASE_URL, json=product_data, headers=api_key_headers)


@when(
    parsers.parse('I try to add a new product with sku "{sku}"'),
    target_fixture="response",
)
def add_duplicate_product_step(client, sku, api_key_headers):
    product_data = {
        "sku": sku,
        "name": "Duplicate Product",
        "description": "This is a duplicate product.",
        "price": 25.00,
        "brand": "DuplicateBrand",
        "category": "DuplicateCategory",
        "stock": 5,
    }
    return client.post(BASE_URL, json=product_data, headers=api_key_headers)


@when(
    parsers.parse('I edit the product "{sku}" with the following details:'),
    target_fixture="response",
)
def edit_product_step(client, sku, datatable, api_key_headers):
    headers = [h.lower() for h in datatable[0]]
    row_values = datatable[1]
    update_data = {
        header: value.strip('"') for header, value in zip(headers, row_values)
    }
    if "price" in update_data:
        update_data["price"] = float(update_data["price"])
    return client.put(
        f"{BASE_URL}/{sku.strip('"')}", json=update_data, headers=api_key_headers
    )


@when(parsers.parse('I remove the product with sku "{sku}"'), target_fixture="response")
def remove_product_step(client, sku, api_key_headers):
    return client.delete(f"{BASE_URL}/{sku.strip('"')}", headers=api_key_headers)


@when("I try to add a product without an API key", target_fixture="response")
def add_product_without_key(client):
    return client.post(
        BASE_URL,
        json={
            "sku": "PROD456",
            "name": "Another Product",
            "description": "Another test product",
            "price": 20.0,
            "brand": "AnotherBrand",
            "category": "AnotherCategory",
            "stock": 5,
        },
    )


@when("I add a new product with the API key", target_fixture="response")
def add_product_with_key(client, api_key_headers):
    return client.post(
        BASE_URL,
        json={
            "sku": "PROD456",
            "name": "Another Product",
            "description": "Another test product",
            "price": 20.0,
            "brand": "AnotherBrand",
            "category": "AnotherCategory",
            "stock": 5,
        },
        headers=api_key_headers,
    )


@when("I try to edit the product without an API key", target_fixture="response")
def edit_product_without_key(client):
    return client.put(f"{BASE_URL}/PROD123", json={"name": "Updated Name"})


@when("I edit the product with the API key", target_fixture="response")
def edit_product_with_key(client, api_key_headers):
    return client.put(
        f"{BASE_URL}/PROD123", json={"name": "Updated Name"}, headers=api_key_headers
    )


@when("I try to remove the product without an API key", target_fixture="response")
def remove_product_without_key(client):
    return client.delete(f"{BASE_URL}/PROD123")


@when("I remove the product with the API key", target_fixture="response")
def remove_product_with_key(client, api_key_headers):
    return client.delete(f"{BASE_URL}/PROD123", headers=api_key_headers)


# --- Then ---


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


@then(parsers.parse('the product "{sku}" should have the updated details'))
def product_should_have_updated_details(client, sku, response):
    updated_data = response.json()
    get_response = client.get(f"{BASE_URL}/{sku.strip('"')}")
    assert get_response.status_code == 200
    product_in_system = get_response.json()
    for key, value in updated_data.items():
        assert product_in_system[key] == value


@then(parsers.parse('the product "{sku}" should not be available in the system'))
def product_should_not_be_available(client, sku):
    response = client.get(f"{BASE_URL}/{sku.strip('"')}")
    assert response.status_code == 404


@then("the request should be denied")
def request_denied(response):
    assert response.status_code == 403


@then("the product should be added successfully")
def product_added(response):
    assert response.status_code == 201
    assert response.json()["sku"] == "PROD456"


@then("the edit request should be denied")
def edit_denied(response):
    assert response.status_code == 403


@then("the product should be updated successfully")
def product_updated(response):
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


@then("the removal request should be denied")
def removal_denied(response):
    assert response.status_code == 403


@then("the product should be removed successfully")
def product_removed(response):
    assert response.status_code == 204
