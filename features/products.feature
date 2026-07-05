Feature: Products

  @smoke
  Scenario: User can see all products on the inventory page
    Given User is logged in with valid credentials
    Then User sees all products listed

  @regression
  Scenario: User can add products to the cart
    Given User is logged in with valid credentials
    When User adds "Sauce Labs Backpack" to the cart
    Then Cart badge shows a count of 1
    When User adds "Sauce Labs Bike Light" to the cart
    Then Cart badge shows a count of 2

  @regression
  Scenario: User can remove a product from the cart
    Given User is logged in with valid credentials and has added a product to the cart
    When User removes "Sauce Labs Backpack" from the cart
    Then Cart badge shows a count of zero
