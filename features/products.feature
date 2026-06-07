Feature: Products

  @smoke
  Scenario: User can see all products on the inventory page
    Given User is logged in with valid credentials
    When Step 1: User views the products page
    Then Step 1: User sees 6 products listed

  @regression
  Scenario: User can add a product to cart
    Given User is logged in with valid credentials
    When Step 1: User adds "Sauce Labs Backpack" to cart
    Then Step 1: User sees the cart badge with count 1
    When Step 2: User adds "Sauce Labs Bike Light" to cart
    Then Step 2: User sees the cart badge with count 2

  @regression
  Scenario: User can remove a product from cart
    Given User is logged in with valid credentials
    And User has added "Sauce Labs Backpack" to cart
    When Step 1: User removes "Sauce Labs Backpack" from cart
    Then Step 1: User sees the cart badge with count 0
