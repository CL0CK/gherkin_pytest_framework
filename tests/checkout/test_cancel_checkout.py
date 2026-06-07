from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import ElementDTO


@Gherkin("checkout.feature", "User cancels checkout and returns to cart")
def test_cancel_checkout(login_page: LoginPage, products_page: ProductsPage, cart_page: CartPage, checkout_page: CheckoutPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")
        login_page.login("standard_user", "secret_sauce")
        products_page.add_product_to_cart_by_name("Sauce Labs Backpack")

    with steps.step(1):
        with steps.when():
            products_page.click_cart_icon()
            cart_page.click_checkout()
        with steps.then():
            checker.check_presence(checkout_page.FIRST_NAME_INPUT, ElementDTO(is_visible=True))

    with steps.step(2):
        with steps.when():
            checkout_page.click_cancel()
        with steps.then():
            checker.check_presence(cart_page.TITLE, ElementDTO(is_visible=True))
