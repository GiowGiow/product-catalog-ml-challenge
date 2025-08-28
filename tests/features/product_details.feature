Feature: Product Details
  As a user,
  I want to be able to view the details of a product,
  So that I can get more information about it.

  Scenario: Retrieve product details
    Given a product with sku "SKU123" exists
    When I request the product details for sku "SKU123"
    Then I should receive the details for "Product 1"
