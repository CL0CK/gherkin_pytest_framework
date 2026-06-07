Feature: Checkout

  @smoke @critical
  Scenario: User completes full checkout flow
    Given User is logged in with valid credentials
    And User has added "Sauce Labs Backpack" to cart
    When Step 1: User clicks on the cart icon
    Then Step 1: User sees the cart page
    When Step 2: User clicks Checkout
    Then Step 2: User sees the checkout information page
    When Step 3: User enters valid information and clicks continue
    Then Step 3: User sees the checkout overview page
    When Step 4: User clicks Finish
    Then Step 4: User sees the success message

  @regression
  Scenario: User cancels checkout and returns to cart
    Given User is logged in with valid credentials
    And User has added "Sauce Labs Backpack" to cart
    When Step 1: User navigates to checkout information page
    Then Step 1: User sees the checkout information page
    When Step 2: User clicks Cancel
    Then Step 2: User is redirected to the cart page
