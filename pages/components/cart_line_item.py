from pages.components.base_component import Component
from utils.element import Element


class CartLineItem(Component):
    ITEM_NAME = Element(".cart_item_label")

    def get_name(self) -> str:
        return self._root.locator(self.ITEM_NAME.selector).text_content() or ""
