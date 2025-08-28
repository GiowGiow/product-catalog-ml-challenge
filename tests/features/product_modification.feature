Feature: Product Modification
  As an administrator,
  I want to edit and remove products,
  So that I can manage the product catalog.

  Background:
    Given the system has the following products:
      | sku      | name          | description              | price | brand   | category | stock |
      | "EDITME" | "Editable"    | "An item to be edited."  | 25.00 | "EditCo"| "Edits"  | 20    |
      | "DELME"  | "Deletable"   | "An item to be deleted." | 15.00 | "DelCo" | "Deletes"| 10    |

  Scenario: Successfully edit an existing product
    When I edit the product "EDITME" with the following details:
      | name          | description              | price |
      | "Updated"     | "This has been updated." | 30.00 |
    Then the response status code should be 200
    And the product "EDITME" should have the updated details

  Scenario: Attempt to edit a non-existent product
    When I edit the product "NONEXISTENT" with the following details:
      | name          | description           | price |
      | "Doesnt Exist"| "This should fail."   | 1.00  |
    Then the response status code should be 404
    And the response should contain an error message "Product with SKU NONEXISTENT not found"

  Scenario: Successfully remove an existing product
    When I remove the product with sku "DELME"
    Then the response status code should be 204
    And the product "DELME" should not be available in the system

  Scenario: Attempt to remove a non-existent product
    When I remove the product with sku "NONEXISTENT"
    Then the response status code should be 404
    And the response should contain an error message "Product with SKU NONEXISTENT not found"
