from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("login.feature", "Successful login with valid credentials")
def test_successful_login(
    login_page: LoginPage, products_page: ProductsPage, cart_page: CartPage, steps: Steps, checker
) -> None:
    with steps.given():
        login_page.navigate("/")

    with steps.step(1):
        with steps.when():
            login_page.login("standard_user", "secret_sauce")
        with steps.then():
            checker.common.check_presence(products_page.PRODUCT_CONTAINER, ElementDTO(is_visible=True))

    with steps.step(2):
        with steps.when():
            products_page.click_cart_icon()
        with steps.then():
            checker.common.check_presence(cart_page.TITLE, ElementDTO(is_visible=True))
