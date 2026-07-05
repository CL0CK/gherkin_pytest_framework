from playwright.sync_api import Locator

from utils.element import Element


class CartLineItem:
    ITEM_NAME = Element(".cart_item_label")

    def __init__(self, root: Locator) -> None:
        self._root = root

    def get_name(self) -> str:
        return self._root.locator(self.ITEM_NAME.selector).text_content() or ""
