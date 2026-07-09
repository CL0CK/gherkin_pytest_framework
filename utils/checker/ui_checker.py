from playwright.sync_api import Page

from utils.checker.checkers.accessibility_checker import AccessibilityChecker
from utils.checker.checkers.button_checker import ButtonChecker
from utils.checker.checkers.common_checker import CommonChecker
from utils.checker.checkers.count_checker import CountChecker
from utils.checker.checkers.image_checker import ImageChecker
from utils.checker.checkers.text_checker import TextChecker


class UIChecker:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.common = CommonChecker(self._page)
        self.text = TextChecker(self._page)
        self.button = ButtonChecker(self._page)
        self.count = CountChecker(self._page)
        self.image = ImageChecker(self._page)
        self.accessibility = AccessibilityChecker(self._page)
