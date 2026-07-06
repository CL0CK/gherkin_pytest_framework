from playwright.sync_api import Locator

from utils.checker.checkers.common_checker import CommonChecker
from utils.checker.dto import ButtonElementDTO
from utils.element import Element


class ButtonChecker(CommonChecker):
    def check(self, element: Element | Locator, dto: ButtonElementDTO) -> None:
        if dto.value_text is not None:
            self.check_attribute(element, "text", dto.value_text, getattr(dto, "contains_text", False), dto.timeout)
        if dto.with_color_check and dto.expected_color is not None:
            self.check_color(element, dto.expected_color, dto.timeout)
