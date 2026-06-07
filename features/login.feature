Feature: Login

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given User is on the SauceDemo login page
    When Step 1: User enters valid credentials and clicks login
    Then Step 1: User is redirected to the products page
    When Step 2: User clicks on the cart icon
    Then Step 2: User is redirected to the cart page

  @smoke @critical
  Scenario: Login with locked out user
    Given User is on the SauceDemo login page
    When Step 1: User enters locked out user credentials and clicks login
    Then Step 1: User sees an error message

  @smoke
  Scenario: Login with empty credentials
    Given User is on the SauceDemo login page
    When Step 1: User clicks login without entering credentials
    Then Step 1: User sees an error message

  @smoke
  Scenario: Login with invalid credentials
    Given User is on the SauceDemo login page
    When Step 1: User enters invalid credentials and clicks login
    Then Step 1: User sees an error message
