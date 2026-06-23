from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import ElementDTO
from utils.markers import regression


@regression
@Gherkin("products.feature", "User can remove a product from cart")
def test_remove_from_cart(login_page: LoginPage, products_page: ProductsPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")
        login_page.login("standard_user", "secret_sauce")
        products_page.add_product_to_cart_by_name("Sauce Labs Backpack")

    with steps.step(1):
        with steps.when():
            products_page.remove_product_from_cart_by_name("Sauce Labs Backpack")
        with steps.then():
            checker.check_presence(products_page.CART_BADGE, ElementDTO(is_hidden=True))
