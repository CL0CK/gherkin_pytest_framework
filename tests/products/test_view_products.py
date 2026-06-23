from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.steps_wrapper import Steps, Gherkin
from utils.checker import CountDTO
from utils.markers import smoke


@smoke
@Gherkin("products.feature", "User can see all products on the inventory page")
def test_view_products(login_page: LoginPage, products_page: ProductsPage, steps: Steps, checker) -> None:
    with steps.given():
        login_page.navigate("/")
        login_page.login("standard_user", "secret_sauce")

    with steps.step(1):
        with steps.when():
            pass
        with steps.then():
            checker.check_count(products_page.PRODUCT_CONTAINER, CountDTO(expected=6))
