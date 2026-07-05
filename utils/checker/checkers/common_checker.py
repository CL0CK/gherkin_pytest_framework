import time

from playwright.sync_api import Locator, Page

from utils.allure.step import CheckStep
from utils.checker.dto import ElementDTO
from utils.element import Element


class CommonChecker:
    def __init__(self, page: Page) -> None:
        self._page = page

    def _locator(self, element: Element) -> Locator:
        return self._page.locator(element.selector)

    @CheckStep
    def check_presence(self, element: Element, dto: ElementDTO) -> None:
        locator = self._locator(element)
        if dto.is_visible and not dto.is_hidden:
            locator.first.wait_for(state="visible", timeout=dto.timeout)
        if dto.is_hidden and not dto.is_visible:
            self._wait_hidden(locator, dto.timeout)

    def _wait_hidden(self, locator: Locator, timeout: int) -> None:
        end = time.time() + timeout / 1000
        while time.time() < end:
            try:
                count = locator.count
                if count == 0:
                    return
            except Exception:
                return
            time.sleep(0.2)
        raise TimeoutError(f"Element still visible after {timeout}ms")

    @CheckStep
    def check_attribute(
        self,
        element: Element,
        attribute: str,
        expected_value: str,
        contains: bool = False,
        timeout: int = 5000,
    ) -> None:
        locator = self._locator(element)
        if attribute == "text":
            actual = locator.text_content(timeout=timeout) or ""
        else:
            actual = locator.get_attribute(attribute, timeout=timeout) or ""
        if contains:
            assert expected_value in actual, f"Expected '{expected_value}' to be in '{actual}'"
        else:
            assert actual == expected_value, f"Expected '{expected_value}', got '{actual}'"

    @CheckStep
    def check_color(
        self,
        element: Element,
        expected_color: str,
        timeout: int = 5000,
    ) -> None:
        locator = self._locator(element)
        actual_color = locator.evaluate("el => window.getComputedStyle(el).color")
        assert actual_color == expected_color, f"Expected color '{expected_color}', got '{actual_color}'"
