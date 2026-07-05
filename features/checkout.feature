Feature: Checkout

  @smoke @critical
  Scenario: User completes full checkout flow
    Given User is logged in, has added a product to the cart, and opens the cart
    When User clicks Checkout and fills in valid shipping information
    Then User sees the checkout overview page
    When User clicks Finish
    Then User sees the success message

  @regression
  Scenario: User cancels checkout and returns to cart
    Given User is logged in, has added a product to the cart, and opens the cart
    When User clicks Checkout, then clicks Cancel
    Then User is redirected to the cart page
