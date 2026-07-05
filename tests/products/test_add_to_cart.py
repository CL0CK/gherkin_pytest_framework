from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import TextElementDTO, UIChecker
from utils.markers import regression
from utils.steps_wrapper import Gherkin, Steps


@regression
@Gherkin("products.feature", "User can add products to the cart")
def test_add_to_cart(
    login_page: LoginPage,
    products_page: ProductsPage,
    steps: Steps,
    checker: UIChecker,
    users_data: dict,
    products_data: dict,
) -> None:
    user = users_data["valid_user"]
    first_product = products_data["products"][0]["name"]
    second_product = products_data["products"][1]["name"]

    with steps.given("User is logged in with valid credentials"):
        login_page.navigate("/")
        login_page.login(user["username"], user["password"])

    with steps.step():
        with steps.when(f'User adds "{first_product}" to the cart'):
            products_page.add_product_to_cart_by_name(first_product)
        with steps.then("Cart badge shows a count of 1"):
            checker.text.check(products_page.CART_BADGE, TextElementDTO(value_text="1"))

    with steps.step():
        with steps.when(f'User adds "{second_product}" to the cart'):
            products_page.add_product_to_cart_by_name(second_product)
        with steps.then("Cart badge shows a count of 2"):
            checker.text.check(products_page.CART_BADGE, TextElementDTO(value_text="2"))
