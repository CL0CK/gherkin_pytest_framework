from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.element import Element


class LoginPage(BasePage):
    USERNAME_INPUT = Element("#user-name")
    PASSWORD_INPUT = Element("#password")
    LOGIN_BUTTON = Element("#login-button")
    ERROR_CONTAINER = Element(".login_wrapper-inner")

    def __init__(self, page: Page):
        super().__init__(page)

    def fill_username(self, username: str):
        self.page.fill(self.USERNAME_INPUT, username)

    def fill_password(self, password: str):
        self.page.fill(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
