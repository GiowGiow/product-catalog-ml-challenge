Feature: Product Listing
  As a user,
  I want to list all available products,
  So that I can browse the catalog.

  Scenario: List all products when multiple products exist
    Given the system has the following products:
      | sku     | name      | description   | price | brand  | category | stock |
      | SKU123  | Product 1 | A description | 10.99 | BrandX | CatA     | 50    |
      | SKU456  | Product 2 | B description | 25.50 | BrandY | CatB     | 100   |
    When I request the list of all products
    Then the response status code should be 200
    And the response should contain a list of 2 products

  Scenario: List all products when the catalog is empty
    Given the system has no products
    When I request the list of all products
    Then the response status code should be 200
    And the response should contain an empty list
