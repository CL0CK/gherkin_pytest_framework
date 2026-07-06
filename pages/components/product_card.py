from pages.components.base_component import Component
from utils.element import Element


class ProductCard(Component):
    ADD_TO_CART_BUTTON = Element(".btn_primary")
    REMOVE_BUTTON = Element(".btn_secondary")

    def add_to_cart(self) -> None:
        self._root.locator(self.ADD_TO_CART_BUTTON.selector).click()

    def remove_from_cart(self) -> None:
        self._root.locator(self.REMOVE_BUTTON.selector).click()
