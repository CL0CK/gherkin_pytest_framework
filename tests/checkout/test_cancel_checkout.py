from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, UIChecker
from utils.markers import regression
from utils.steps_wrapper import Gherkin, Steps


@regression
@Gherkin("checkout.feature", "User cancels checkout and returns to cart")
def test_cancel_checkout(
    login_page: LoginPage,
    products_page: ProductsPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
    steps: Steps,
    checker: UIChecker,
    users_data: dict,
    products_data: dict,
) -> None:
    user = users_data["valid_user"]
    product_name = products_data["products"][0]["name"]

    with steps.given("User is logged in, has added a product to the cart, and opens the cart"):
        login_page.navigate("/")
        login_page.login(user["username"], user["password"])
        products_page.product_by_name(product_name).add_to_cart()
        products_page.click_cart_icon()

    with steps.step():
        with steps.when("User clicks Checkout, then clicks Cancel"):
            cart_page.click_checkout()
            checkout_page.click_cancel()
        with steps.then("User is redirected to the cart page"):
            checker.common.check_presence(cart_page.TITLE, ElementDTO(is_visible=True))
