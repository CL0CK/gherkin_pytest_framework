Feature: Login

  @smoke @critical
  Scenario Outline: Login with various credentials
    Given User is on the SauceDemo login page
    When User enters "<username>" and "<password>" and clicks login
    Then User sees "<expected_result>"

    Examples:
      | username      | password       | expected_result   |
      | standard_user | secret_sauce   | products page     |
      | locked_out    | secret_sauce   | error message     |
      |               |                | validation error  |
      | invalid_user  | wrong_pass     | error message     |

  @smoke @critical
  Scenario: Successful login and cart navigation
    Given User is on the SauceDemo login page
    When User enters valid credentials and clicks login
    Then User is redirected to the products page
    When User clicks the cart icon
    Then User is redirected to the cart page
