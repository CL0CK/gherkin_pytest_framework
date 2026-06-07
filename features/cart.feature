Feature: Cart

  @smoke @critical
  Scenario: User can view cart with added products
    Given User is logged in with valid credentials
    And User has added "Sauce Labs Backpack" to cart
    When Step 1: User clicks on the cart icon
    Then Step 1: User sees Sauce Labs Backpack in the cart
    When Step 2: User clicks Continue Shopping
    Then Step 2: User is redirected to the products page

  @regression
  Scenario: User can proceed to checkout from cart
    Given User is logged in with valid credentials
    And User has added "Sauce Labs Backpack" to cart
    When Step 1: User clicks on the cart icon
    Then Step 1: User sees the cart page
    When Step 2: User clicks Checkout
    Then Step 2: User sees the checkout information page
