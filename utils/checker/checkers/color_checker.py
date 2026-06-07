from playwright.sync_api import Locator
from utils.checker.dto import TextElementDTO


class ColorChecker:
    def check(self, locator: Locator, dto: TextElementDTO):
        if dto.expected_color is not None:
            actual_color = locator.evaluate(
                "el => window.getComputedStyle(el).color"
            )
            assert actual_color == dto.expected_color, (
                f"Expected color '{dto.expected_color}', got '{actual_color}'"
            )

    def check_background(self, locator: Locator, expected_color: str):
        actual_color = locator.evaluate(
            "el => window.getComputedStyle(el).backgroundColor"
        )
        assert actual_color == expected_color, (
            f"Expected background '{expected_color}', got '{actual_color}'"
        )
