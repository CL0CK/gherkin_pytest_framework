from playwright.sync_api import Locator, Page

from utils.checker.dto import CountDTO
from utils.element import Element, resolve_locator


class CountChecker:
    def __init__(self, page: Page) -> None:
        self._page = page

    def _locator(self, element: Element | Locator) -> Locator:
        return resolve_locator(self._page, element)

    def check(self, element: Element | Locator, dto: CountDTO) -> None:
        locator = self._locator(element)
        actual_count = locator.count()
        assert actual_count == dto.expected, f"Expected {dto.expected} elements, found {actual_count}"
