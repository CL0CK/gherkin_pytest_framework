from playwright.sync_api import Locator
from utils.checker.dto import TextElementDTO


class TextChecker:
    def check(self, locator: Locator, dto: TextElementDTO):
        self._check_text(locator, dto)
        self._check_color(locator, dto)
        self._check_font(locator, dto)

    def _check_text(self, locator: Locator, dto: TextElementDTO):
        if dto.value_text is not None:
            actual_text = locator.text_content(timeout=dto.timeout)
            if dto.contains_text:
                assert dto.value_text in actual_text, (
                    f"Expected '{dto.value_text}' to be in '{actual_text}'"
                )
            else:
                assert actual_text == dto.value_text, (
                    f"Expected '{dto.value_text}', got '{actual_text}'"
                )

    def _check_color(self, locator: Locator, dto: TextElementDTO):
        if dto.with_color_check and dto.expected_color is not None:
            actual_color = locator.evaluate(
                "el => window.getComputedStyle(el).color"
            )
            assert actual_color == dto.expected_color, (
                f"Expected color '{dto.expected_color}', got '{actual_color}'"
            )

    def _check_font(self, locator: Locator, dto: TextElementDTO):
        if dto.with_font_check:
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
