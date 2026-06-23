from playwright.sync_api import Page
from utils.element import Element
from utils.allure import allure_step
from utils.logger.logger import get_logger

logger = get_logger()


class PageLogger:
    def __init__(self, page: Page):
        self._page = page

    def _resolve(self, selector):
        if isinstance(selector, Element):
            return selector.selector, selector.name
        return selector, selector

    def _log(self, action: str, name: str, extra: str = ""):
        msg = f"  ✓ {action}({name}"
        if extra:
            msg += f", {extra}"
        msg += ")"
        logger.info(msg)

    @allure_step
    def fill(self, selector, value):
        sel, name = self._resolve(selector)
        self._log("fill", name, repr(value))
        return self._page.fill(sel, value)

    @allure_step
    def click(self, selector):
        sel, name = self._resolve(selector)
        self._log("click", name)
        return self._page.click(sel)

    @allure_step
    def goto(self, url: str, **kwargs):
        self._log("goto", url)
        return self._page.goto(url, **kwargs)

    @allure_step
    def wait_for_selector(self, selector, **kwargs):
        sel, name = self._resolve(selector)
        self._log("wait_for_selector", name, str(kwargs))
        return self._page.wait_for_selector(sel, **kwargs)

    @allure_step
    def wait_for_url(self, url, **kwargs):
        self._log("wait_for_url", url)
        return self._page.wait_for_url(url, **kwargs)

    @allure_step
    def wait_for_load_state(self, state: str = "load"):
        self._log("wait_for_load_state", state)
        return self._page.wait_for_load_state(state)

    def locator(self, selector):
        return self._page.locator(selector)

    @allure_step
    def is_visible(self, selector, **kwargs):
        sel, name = self._resolve(selector)
        self._log("is_visible", name)
        return self._page.is_visible(sel, **kwargs)

    @allure_step
    def text_content(self, selector):
        sel, name = self._resolve(selector)
        self._log("text_content", name)
        return self._page.text_content(sel)

    @allure_step
    def screenshot(self, **kwargs):
        self._log("screenshot", "")
        return self._page.screenshot(**kwargs)

    def evaluate(self, expression: str, *args):
        return self._page.evaluate(expression, *args)

    def query_selector_all(self, selector):
        return self._page.query_selector_all(selector)

    @property
    def url(self) -> str:
        return self._page.url

    @property
    def title(self) -> str:
        return self._page.title()

    def __getattr__(self, name):
        return getattr(self._page, name)
