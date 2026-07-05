from playwright.sync_api import Page

from utils.config import Settings
from utils.element import Element
from utils.logger import PageLogger


class BasePage:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, Element) and not attr_value._name:
                attr_value._name = attr_name

    def __init__(self, page: Page, config: Settings | None = None):
        self.page = PageLogger(page)
        self.config = config or Settings()

    def navigate(self, path: str = "/"):
        url = f"{self.config.base_url}{path}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_url(self) -> str:
        return self.page.url

    def wait_for_url(self, expected_path: str, timeout: int = 5000):
        self.page.wait_for_url(lambda url: expected_path in url, timeout=timeout)

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        return self.page.screenshot(full_page=True)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = 5000):
        return self.page.wait_for_selector(selector, state=state, timeout=timeout)
