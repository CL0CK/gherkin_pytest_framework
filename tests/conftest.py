import pytest
import yaml
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.steps_wrapper import Steps
from utils.checker import UIChecker


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture(scope="function")
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture(scope="function")
def steps() -> Steps:
    return Steps()


@pytest.fixture(scope="function")
def checker(page: Page) -> UIChecker:
    return UIChecker(page)


@pytest.fixture(scope="session")
def users_data() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "users.yaml"
    with open(data_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def products_data() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "products.yaml"
    with open(data_path, "r") as f:
        return yaml.safe_load(f)
