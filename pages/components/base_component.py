from playwright.sync_api import Locator

from utils.element import Element


class Component:
    """
    Base class for Component Objects (a repeated widget scoped to one root
    Locator, e.g. a single product card or cart line item — as opposed to a
    Page Object, which represents a whole route/page).

    `.locator(element)` resolves an Element's selector *within this
    component's root*, returning a real Playwright Locator. Pass that
    Locator (not the bare Element) to checker.* calls to keep assertions
    scoped the same way actions already are — see utils/element.py's
    resolve_locator() for why this matters.
    """

    def __init__(self, root: Locator) -> None:
        self._root = root

    def locator(self, element: Element) -> Locator:
        return self._root.locator(element.selector)
