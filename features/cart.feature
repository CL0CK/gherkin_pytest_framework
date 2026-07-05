Feature: Cart

  @smoke @critical
  Scenario: User can view cart with added products
    Given User is logged in with valid credentials and has added a product to the cart
    When User clicks on the cart icon
    Then User sees the added product in the cart
    When User clicks Continue Shopping
    Then User is redirected to the products page

  @regression
  Scenario: User can proceed to checkout from cart
    Given User is logged in with valid credentials and has added a product to the cart
    When User clicks on the cart icon
    Then User sees the cart page
    When User clicks Checkout
    Then User sees the checkout information page
