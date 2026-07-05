from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import ElementDTO, UIChecker
from utils.markers import regression
from utils.steps_wrapper import Gherkin, Steps


@regression
@Gherkin("products.feature", "User can remove a product from the cart")
def test_remove_from_cart(
    login_page: LoginPage,
    products_page: ProductsPage,
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
        products_page.add_product_to_cart_by_name(product_name)

    with steps.step():
        with steps.when(f'User removes "{product_name}" from the cart'):
            products_page.remove_product_from_cart_by_name(product_name)
        with steps.then("Cart badge shows a count of zero"):
            checker.common.check_presence(products_page.CART_BADGE, ElementDTO(is_visible=True, is_hidden=True))
