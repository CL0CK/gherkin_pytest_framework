from playwright.sync_api import Page, Locator

from utils.allure import allure_step
from utils.element import Element
from utils.checker.checkers.text_checker import TextChecker
from utils.checker.checkers.presence_checker import PresenceChecker
from utils.checker.checkers.count_checker import CountChecker
from utils.checker.checkers.color_checker import ColorChecker
from utils.checker.checkers.font_checker import FontChecker
from utils.checker.dto import (
    TextElementDTO,
    ButtonElementDTO,
    ImageElementDTO,
    ElementDTO,
    CountDTO,
)
from utils.logger.logger import get_logger

logger = get_logger()


class UIChecker:
    def __init__(self, page: Page):
        self.page = page
        self.text = TextChecker()
        self.presence = PresenceChecker()
        self.count = CountChecker()
        self.color = ColorChecker()
        self.font = FontChecker()

    def _locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def _resolve(self, selector):
        if isinstance(selector, Element):
            return selector.selector, selector.name
        return selector, selector

    def _log_check(self, check_type: str, name: str, dto):
        logger.info(f"  ✓ {check_type}: {name} ({dto})")

    @allure_step
    def check_text(self, selector, dto: TextElementDTO):
        sel, name = self._resolve(selector)
        self._log_check("check_text", name, dto)
        self.text.check(self._locator(sel), dto)

    @allure_step
    def check_button(self, selector, dto: ButtonElementDTO):
        sel, name = self._resolve(selector)
        self._log_check("check_button", name, dto)
        loc = self._locator(sel)
        self.presence.check(loc, dto)
        self.text.check(loc, dto)

    @allure_step
    def check_image(self, selector, dto: ImageElementDTO):
        sel, name = self._resolve(selector)
        self._log_check("check_image", name, dto)
        loc = self._locator(sel)
        self.presence.check(loc, dto)
        if dto.src_contains is not None:
            actual_src = loc.get_attribute("src")
            assert dto.src_contains in actual_src, (
                f"Expected '{dto.src_contains}' in src '{actual_src}'"
            )
        if dto.alt_text is not None:
            actual_alt = loc.get_attribute("alt")
            assert actual_alt == dto.alt_text, (
                f"Expected alt '{dto.alt_text}', got '{actual_alt}'"
            )

    @allure_step
    def check_presence(self, selector, dto: ElementDTO):
        sel, name = self._resolve(selector)
        self._log_check("check_presence", name, dto)
        self.presence.check(self._locator(sel), dto)

    @allure_step
    def check_count(self, selector, dto: CountDTO):
        sel, name = self._resolve(selector)
        self._log_check("check_count", name, dto)
        self.count.check(self._locator(sel), dto)
