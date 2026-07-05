from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import CountDTO, UIChecker
from utils.markers import smoke
from utils.steps_wrapper import Gherkin, Steps


@smoke
@Gherkin("products.feature", "User can see all products on the inventory page")
def test_view_products(
    login_page: LoginPage, products_page: ProductsPage, steps: Steps, checker: UIChecker, users_data: dict
) -> None:
    user = users_data["valid_user"]

    with steps.given("User is logged in with valid credentials"):
        login_page.navigate("/")
        login_page.login(user["username"], user["password"])

    with steps.step():
        with steps.then("User sees all products listed"):
            checker.count.check(products_page.PRODUCT_CONTAINER, CountDTO(expected=6))
