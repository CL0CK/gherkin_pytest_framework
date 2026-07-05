from pathlib import Path

from playwright.sync_api import Page
import pytest
import yaml

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.checker import UIChecker
from utils.config import Settings
from utils.steps_wrapper import Steps


@pytest.fixture(scope="function")
def login_page(page: Page, config: Settings) -> LoginPage:
    return LoginPage(page, config)


@pytest.fixture(scope="function")
def products_page(page: Page, config: Settings) -> ProductsPage:
    return ProductsPage(page, config)


@pytest.fixture(scope="function")
def cart_page(page: Page, config: Settings) -> CartPage:
    return CartPage(page, config)


@pytest.fixture(scope="function")
def checkout_page(page: Page, config: Settings) -> CheckoutPage:
    return CheckoutPage(page, config)


@pytest.fixture(scope="function")
def steps() -> Steps:
    return Steps()


@pytest.fixture(scope="function")
def checker(page: Page) -> UIChecker:
    return UIChecker(page)


@pytest.fixture(scope="session")
def users_data() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "users.yaml"
    with open(data_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def products_data() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "products.yaml"
    with open(data_path) as f:
        return yaml.safe_load(f)
