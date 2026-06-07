from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import TextElementDTO


@Gherkin("products.feature", "User can add a product to cart")
def test_add_to_cart(login_page: LoginPage, products_page: ProductsPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")
        login_page.login("standard_user", "secret_sauce")

    with steps.step(1):
        with steps.when():
            products_page.add_product_to_cart_by_name("Sauce Labs Backpack")
        with steps.then():
            checker.check_text(products_page.CART_BADGE, TextElementDTO(value_text="1"))

    with steps.step(2):
        with steps.when():
            products_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
        with steps.then():
            checker.check_text(products_page.CART_BADGE, TextElementDTO(value_text="2"))
