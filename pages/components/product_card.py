from playwright.sync_api import Locator

from utils.element import Element


class ProductCard:
    ADD_TO_CART_BUTTON = Element(".btn_primary")
    REMOVE_BUTTON = Element(".btn_secondary")

    def __init__(self, root: Locator) -> None:
        self._root = root

    def add_to_cart(self) -> None:
        self._root.locator(self.ADD_TO_CART_BUTTON.selector).click()

    def remove_from_cart(self) -> None:
        self._root.locator(self.REMOVE_BUTTON.selector).click()
