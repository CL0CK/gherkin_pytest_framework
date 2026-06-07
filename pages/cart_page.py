from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.element import Element


class CartPage(BasePage):
    CART_ITEM = Element(".cart_item")
    CART_ITEM_NAME = Element(".cart_item_label")
    CHECKOUT_BUTTON = Element("#checkout")
    CONTINUE_SHOPPING_BUTTON = Element("#continue-shopping")
    TITLE = Element(".title")

    def __init__(self, page: Page):
        super().__init__(page)

    def click_checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        self.page.click(self.CONTINUE_SHOPPING_BUTTON)
