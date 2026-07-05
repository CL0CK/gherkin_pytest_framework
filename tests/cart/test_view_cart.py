from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, TextElementDTO, UIChecker
from utils.markers import critical, smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@critical
@Gherkin("cart.feature", "User can view cart with added products")
def test_view_cart(
    login_page: LoginPage,
    products_page: ProductsPage,
    cart_page: CartPage,
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
        with steps.then("User sees the added product in the cart"):
            dto = TextElementDTO(value_text=product_name, contains_text=True)
            checker.text.check(cart_page.cart_line_item().ITEM_NAME, dto)

    with steps.step():
        with steps.when("User clicks Continue Shopping"):
            cart_page.click_continue_shopping()
        with steps.then("User is redirected to the products page"):
            checker.common.check_presence(products_page.PRODUCT_CONTAINER, ElementDTO(is_visible=True))
