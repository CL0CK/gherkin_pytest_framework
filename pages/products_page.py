from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components import ProductCard
from utils.config import Settings
from utils.element import Element


class ProductsPage(BasePage):
    PRODUCT_CONTAINER = Element(".inventory_item")
    PRODUCT_NAME = Element(".inventory_item_name")
    CART_BADGE = Element(".shopping_cart_badge")
    CART_ICON = Element(".shopping_cart_link")
    MENU_BUTTON = Element("#react-burger-menu-btn")
    LOGOUT_BUTTON = Element("#logout_sidebar_link")

    def __init__(self, page: Page, config: Settings | None = None):
        super().__init__(page, config)

    def product_by_name(self, product_name: str) -> ProductCard:
        product_row = self.page.locator(".inventory_item").filter(has_text=product_name)
        return ProductCard(product_row)

    def click_cart_icon(self):
        self.page.click(self.CART_ICON)

    def click_menu_button(self):
        self.page.click(self.MENU_BUTTON)

    def click_logout(self):
        self.click_menu_button()
        self.page.click(self.LOGOUT_BUTTON)
