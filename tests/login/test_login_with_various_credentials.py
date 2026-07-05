from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, TextElementDTO, UIChecker
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("login.feature", "Login with various credentials")
def test_login_with_various_credentials(
    login_page: LoginPage,
    products_page: ProductsPage,
    steps: Steps,
    checker: UIChecker,
    username: str,
    password: str,
    expected_result: str,
) -> None:
    with steps.given("User is on the SauceDemo login page"):
        login_page.navigate("/")

    with steps.step():
        with steps.when('User enters "<username>" and "<password>" and clicks login'):
            if username and password:
                login_page.login(username, password)
            else:
                login_page.click_login()

        with steps.then('User sees "<expected_result>"'):
            if expected_result == "products page":
                checker.common.check_presence(products_page.PRODUCT_CONTAINER, ElementDTO(is_visible=True))
            elif expected_result == "error message":
                checker.common.check_presence(login_page.ERROR_CONTAINER, ElementDTO(is_visible=True))
            else:
                dto = TextElementDTO(value_text="Username is required", contains_text=True)
                checker.text.check(login_page.ERROR_CONTAINER, dto)
