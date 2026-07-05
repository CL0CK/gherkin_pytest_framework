from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, TextElementDTO, UIChecker
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("checkout.feature", "User completes full checkout flow")
def test_full_checkout(
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
    checkout_info = users_data["checkout"]
    product_name = products_data["products"][0]["name"]

    with steps.given("User is logged in, has added a product to the cart, and opens the cart"):
        login_page.navigate("/")
        login_page.login(user["username"], user["password"])
        products_page.add_product_to_cart_by_name(product_name)
        products_page.click_cart_icon()

    with steps.step():
        with steps.when("User clicks Checkout and fills in valid shipping information"):
            cart_page.click_checkout()
            checkout_page.fill_information(
                checkout_info["first_name"], checkout_info["last_name"], checkout_info["zip_code"]
            )
            checkout_page.click_continue()
        with steps.then("User sees the checkout overview page"):
            checker.common.check_presence(checkout_page.ITEM_OVERVIEW, ElementDTO(is_visible=True))

    with steps.step():
        with steps.when("User clicks Finish"):
            checkout_page.click_finish()
        with steps.then("User sees the success message"):
            checker.common.check_presence(checkout_page.SUCCESS_MESSAGE, ElementDTO(is_visible=True))
            checker.text.check(checkout_page.SUCCESS_MESSAGE, TextElementDTO(value_text="Checkout: Complete!"))
