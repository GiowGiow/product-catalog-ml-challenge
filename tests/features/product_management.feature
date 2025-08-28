Feature: Product Management
  As an administrator,
  I want to add new products to the system,
  So that they are available in the catalog.

  Background:
    Given the system is running

  Scenario: Successfully add a new product
    When I add a new product with the following details:
      | sku         | name         | description              | price | brand     | category       | stock |
      | "NEWPROD"   | "New Gadget" | "A shiny new gadget."    | 99.99 | "GadgetCo"| "Electronics"  | 150   |
    Then the response status code should be 201
    And the product "NEWPROD" should be available in the system

  Scenario: Attempt to add a product with a duplicate SKU
    Given a product with sku "SKU123" exists
    When I try to add a new product with sku "SKU123"
    Then the response status code should be 400
    And the response should contain an error message "Invalid sku SKU123"
