import allure
from playwright.sync_api import Page
from utils.element import Element
from utils.logger import get_logger

logger = get_logger()


class LoggingPage:
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

    def fill(self, selector, value):
        sel, name = self._resolve(selector)
        self._log("fill", name, repr(value))
        with allure.step(f"fill({name}, {value!r})"):
            return self._page.fill(sel, value)

    def click(self, selector):
        sel, name = self._resolve(selector)
        self._log("click", name)
        with allure.step(f"click({name})"):
            return self._page.click(sel)

    def goto(self, url: str, **kwargs):
        self._log("goto", url)
        with allure.step(f"goto({url})"):
            return self._page.goto(url, **kwargs)

    def wait_for_selector(self, selector, **kwargs):
        sel, name = self._resolve(selector)
        self._log("wait_for_selector", name, str(kwargs))
        with allure.step(f"wait_for_selector({name})"):
            return self._page.wait_for_selector(sel, **kwargs)

    def wait_for_url(self, url, **kwargs):
        self._log("wait_for_url", url)
        with allure.step(f"wait_for_url({url})"):
            return self._page.wait_for_url(url, **kwargs)

    def wait_for_load_state(self, state: str = "load"):
        self._log("wait_for_load_state", state)
        with allure.step(f"wait_for_load_state({state})"):
            return self._page.wait_for_load_state(state)

    def locator(self, selector):
        return self._page.locator(selector)

    def is_visible(self, selector, **kwargs):
        sel, name = self._resolve(selector)
        self._log("is_visible", name)
        with allure.step(f"is_visible({name})"):
            return self._page.is_visible(sel, **kwargs)

    def text_content(self, selector):
        sel, name = self._resolve(selector)
        self._log("text_content", name)
        with allure.step(f"text_content({name})"):
            return self._page.text_content(sel)

    def screenshot(self, **kwargs):
        self._log("screenshot", "")
        with allure.step("screenshot"):
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
