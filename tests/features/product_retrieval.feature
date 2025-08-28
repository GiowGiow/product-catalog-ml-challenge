Feature: Product Retrieval
  As a user,
  I want to be able to view product details,
  So that I can make informed purchasing decisions.

  Background:
    Given the system has the following products:
      | sku     | name      | description   | price | brand  | category | stock |
      | SKU123  | Product 1 | A description | 10.99 | BrandX | CatA     | 50    |

  Scenario: Retrieve an existing product's details successfully
    When I request the product details for sku "SKU123"
    Then the response status code should be 200
    And the response should contain the details for the product "SKU123"

  Scenario: Attempt to retrieve a non-existent product
    When I request the product details for sku "NONEXISTENT"
    Then the response status code should be 404
    And the response should contain an error message "Product with SKU NONEXISTENT not found"
