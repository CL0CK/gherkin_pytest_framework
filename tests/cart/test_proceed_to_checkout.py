from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, UIChecker
from utils.markers import regression
from utils.steps_wrapper import Gherkin, Steps


@regression
@Gherkin("cart.feature", "User can proceed to checkout from cart")
def test_proceed_to_checkout(
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

    with steps.given("User is logged in with valid credentials and has added a product to the cart"):
        login_page.navigate("/")
        login_page.login(user["username"], user["password"])
        products_page.product_by_name(product_name).add_to_cart()

    with steps.step():
        with steps.when("User clicks on the cart icon"):
            products_page.click_cart_icon()
        with steps.then("User sees the cart page"):
            checker.common.check_presence(cart_page.TITLE, ElementDTO(is_visible=True))

    with steps.step():
        with steps.when("User clicks Checkout"):
            cart_page.click_checkout()
        with steps.then("User sees the checkout information page"):
            checker.common.check_presence(checkout_page.FIRST_NAME_INPUT, ElementDTO(is_visible=True))
