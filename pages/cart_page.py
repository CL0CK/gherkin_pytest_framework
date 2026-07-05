from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components import CartLineItem
from utils.config import Settings
from utils.element import Element


class CartPage(BasePage):
    CART_ITEM = Element(".cart_item")
    CHECKOUT_BUTTON = Element("#checkout")
    CONTINUE_SHOPPING_BUTTON = Element("#continue-shopping")
    TITLE = Element(".title")

    def __init__(self, page: Page, config: Settings | None = None):
        super().__init__(page, config)

    def cart_line_item(self, index: int = 0) -> CartLineItem:
        item_locator = self.page.locator(self.CART_ITEM.selector).nth(index)
        return CartLineItem(item_locator)

    def click_checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        self.page.click(self.CONTINUE_SHOPPING_BUTTON)
