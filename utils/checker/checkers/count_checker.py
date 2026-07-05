from playwright.sync_api import Page

from utils.checker.dto import CountDTO
from utils.element import Element


class CountChecker:
    def __init__(self, page: Page) -> None:
        self._page = page

    def _locator(self, element: Element):
        return self._page.locator(element.selector)

    def check(self, element: Element, dto: CountDTO) -> None:
        locator = self._locator(element)
        actual_count = locator.count() if callable(locator.count) else locator.count
        assert actual_count == dto.expected, f"Expected {dto.expected} elements, found {actual_count}"
