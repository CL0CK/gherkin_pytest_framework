from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, UIChecker
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("login.feature", "Successful login and cart navigation")
def test_successful_login(
    login_page: LoginPage,
    products_page: ProductsPage,
    cart_page: CartPage,
    steps: Steps,
    checker: UIChecker,
    users_data: dict,
) -> None:
    user = users_data["valid_user"]

    with steps.given("User is on the SauceDemo login page"):
        login_page.navigate("/")

    with steps.step():
        with steps.when("User enters valid credentials and clicks login"):
            login_page.login(user["username"], user["password"])
        with steps.then("User is redirected to the products page"):
            checker.common.check_presence(products_page.PRODUCT_CONTAINER, ElementDTO(is_visible=True))

    with steps.step():
        with steps.when("User clicks the cart icon"):
            products_page.click_cart_icon()
        with steps.then("User is redirected to the cart page"):
            checker.common.check_presence(cart_page.TITLE, ElementDTO(is_visible=True))
