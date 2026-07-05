from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.config import Settings
from utils.element import Element


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = Element("#first-name")
    LAST_NAME_INPUT = Element("#last-name")
    ZIP_CODE_INPUT = Element("#postal-code")
    CONTINUE_BUTTON = Element("#continue")
    CANCEL_BUTTON = Element("#cancel")
    TOTAL_LABEL = Element(".summary_subtotal_label")
    TOTAL_VALUE = Element(".summary_subtotal_cost")
    FINISH_BUTTON = Element("#finish")
    ITEM_OVERVIEW = Element(".cart_item")
    SUCCESS_MESSAGE = Element(".title")
    SUCCESS_ICON = Element(".hero-graphic")
    BACK_TO_HOME_BUTTON = Element("#back-to-products")

    def __init__(self, page: Page, config: Settings | None = None):
        super().__init__(page, config)

    def fill_information(self, first_name: str, last_name: str, zip_code: str):
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.ZIP_CODE_INPUT, zip_code)

    def click_continue(self):
        self.page.click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        self.page.click(self.CANCEL_BUTTON)

    def click_finish(self):
        self.page.click(self.FINISH_BUTTON)

    def click_back_to_home(self):
        self.page.click(self.BACK_TO_HOME_BUTTON)
