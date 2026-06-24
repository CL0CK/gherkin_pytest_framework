from utils.checker.checkers.button_checker import ButtonChecker
from utils.checker.checkers.common_checker import CommonChecker
from utils.checker.checkers.count_checker import CountChecker
from utils.checker.checkers.text_checker import TextChecker


class UIChecker:
    def __init__(self) -> None:
        self.common = CommonChecker()
        self.text = TextChecker()
        self.button = ButtonChecker()
        self.count = CountChecker()
