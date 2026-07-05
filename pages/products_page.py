from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.element import Element


class ProductsPage(BasePage):
    PRODUCT_CONTAINER = Element(".inventory_item")
    PRODUCT_NAME = Element(".inventory_item_name")
    ADD_TO_CART_BUTTON = Element(".btn_primary")
    REMOVE_BUTTON = Element(".btn_secondary")
    CART_BADGE = Element(".shopping_cart_badge")
    CART_ICON = Element(".shopping_cart_link")
    MENU_BUTTON = Element("#react-burger-menu-btn")
    LOGOUT_BUTTON = Element("#logout_sidebar_link")

    def __init__(self, page: Page):
        super().__init__(page)

    def add_product_to_cart_by_name(self, product_name: str):
        product_row = self.page.locator(".inventory_item").filter(has_text=product_name)
        add_btn = product_row.locator(self.ADD_TO_CART_BUTTON.selector)
        add_btn.click()

    def remove_product_from_cart_by_name(self, product_name: str):
        product_row = self.page.locator(".inventory_item").filter(has_text=product_name)
        remove_btn = product_row.locator(self.REMOVE_BUTTON.selector)
        remove_btn.click()

    def click_cart_icon(self):
        self.page.click(self.CART_ICON)

    def click_menu_button(self):
        self.page.click(self.MENU_BUTTON)

    def click_logout(self):
        self.click_menu_button()
        self.page.click(self.LOGOUT_BUTTON)
