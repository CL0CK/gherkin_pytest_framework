from utils.checker.dto import CountDTO
from utils.element import Element


class CountChecker:
    def check(self, element: Element, dto: CountDTO) -> None:
        locator = element.locator()
        actual_count = locator.count() if callable(locator.count) else locator.count
        assert actual_count == dto.expected, f"Expected {dto.expected} elements, found {actual_count}"
