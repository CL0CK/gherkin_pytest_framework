from utils.allure.step import CheckStep
from utils.checker.checkers.common_checker import CommonChecker
from utils.checker.dto import TextElementDTO
from utils.element import Element


class TextChecker(CommonChecker):
    @CheckStep
    def check_text(
        self,
        element: Element,
        value_text: str,
        contains_text: bool = False,
        timeout: int = 5000,
    ) -> None:
        locator = self._locator(element)
        actual_text = locator.text_content(timeout=timeout)
        if actual_text is None:
            actual_text = ""
        if contains_text:
            assert value_text in actual_text, f"Expected '{value_text}' to be in '{actual_text}'"
        else:
            assert actual_text == value_text, f"Expected '{value_text}', got '{actual_text}'"

    @CheckStep
    def check_font(
        self,
        element: Element,
        expected_font_family: str | None = None,
        expected_font_size: str | None = None,
        timeout: int = 5000,
    ) -> None:
        locator = self._locator(element)
        if expected_font_family is not None:
            actual_family = locator.evaluate("el => window.getComputedStyle(el).fontFamily")
            assert (
                expected_font_family.lower() in actual_family.lower()
            ), f"Expected font family '{expected_font_family}', got '{actual_family}'"
        if expected_font_size is not None:
            actual_size = locator.evaluate("el => window.getComputedStyle(el).fontSize")
            assert (
                actual_size == expected_font_size
            ), f"Expected font size '{expected_font_size}', got '{actual_size}'"

    def check(self, element: Element, dto: TextElementDTO) -> None:
        if dto.value_text is not None:
            self.check_text(element, dto.value_text, dto.contains_text, dto.timeout)
        if dto.with_color_check and dto.expected_color is not None:
            self.check_color(element, dto.expected_color, dto.timeout)
        if dto.with_font_check:
            self.check_font(
                element,
                dto.expected_font_family,
                dto.expected_font_size,
                dto.timeout,
            )
