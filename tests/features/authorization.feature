Feature: API Authorization

  Scenario: Attempt to add a product without API key
    When I try to add a product without an API key
    Then the request should be denied

  Scenario: Successfully add a product with API key
    When I add a new product with the API key
    Then the product should be added successfully

  Scenario: Attempt to edit a product without API key
    Given a product exists
    When I try to edit the product without an API key
    Then the edit request should be denied

  Scenario: Successfully edit a product with API key
    Given a product exists
    When I edit the product with the API key
    Then the product should be updated successfully

  Scenario: Attempt to remove a product without API key
    Given a product exists
    When I try to remove the product without an API key
    Then the removal request should be denied

  Scenario: Successfully remove a product with API key
    Given a product exists
    When I remove the product with the API key
    Then the product should be removed successfully
