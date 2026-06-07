from playwright.sync_api import Locator
from utils.checker.dto import TextElementDTO


class FontChecker:
    def check(self, locator: Locator, dto: TextElementDTO):
        if dto.expected_font_family is not None:
            actual_family = locator.evaluate(
                "el => window.getComputedStyle(el).fontFamily"
            )
            assert dto.expected_font_family.lower() in actual_family.lower(), (
                f"Expected font family '{dto.expected_font_family}', "
                f"got '{actual_family}'"
            )
        if dto.expected_font_size is not None:
            actual_size = locator.evaluate(
                "el => window.getComputedStyle(el).fontSize"
            )
            assert actual_size == dto.expected_font_size, (
                f"Expected font size '{dto.expected_font_size}', "
                f"got '{actual_size}'"
            )
