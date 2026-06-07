from playwright.sync_api import Locator
from utils.checker.dto import CountDTO


class CountChecker:
    def check(self, locator: Locator, dto: CountDTO):
        actual_count = locator.count() if callable(locator.count) else locator.count
        assert actual_count == dto.expected, (
            f"Expected {dto.expected} elements, found {actual_count}"
        )
