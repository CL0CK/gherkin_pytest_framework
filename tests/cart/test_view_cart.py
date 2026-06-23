from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import ElementDTO, TextElementDTO
from utils.markers import smoke, critical


@smoke
@critical
@Gherkin("cart.feature", "User can view cart with added products")
def test_view_cart(login_page: LoginPage, products_page: ProductsPage, cart_page: CartPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")
        login_page.login("standard_user", "secret_sauce")
        products_page.add_product_to_cart_by_name("Sauce Labs Backpack")

    with steps.step(1):
        with steps.when():
            products_page.click_cart_icon()
        with steps.then():
            checker.check_text(cart_page.CART_ITEM_NAME, TextElementDTO(value_text="Sauce Labs Backpack", contains_text=True))

    with steps.step(2):
        with steps.when():
            cart_page.click_continue_shopping()
        with steps.then():
            checker.check_presence(products_page.PRODUCT_CONTAINER, ElementDTO(is_visible=True))
