from typing import Any, Literal

from playwright.sync_api import ElementHandle, Locator, Page

from utils.allure import allure_step
from utils.element import Element
from utils.logger.logger import get_logger

logger = get_logger()


class PageLogger:
    def __init__(self, page: Page):
        self._page = page

    def _resolve(self, selector: str | Element) -> tuple[str, str]:
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
    def fill(self, selector: str | Element, value: str) -> None:
        sel, name = self._resolve(selector)
        self._log("fill", name, repr(value))
        self._page.fill(sel, value)

    @allure_step
    def click(self, selector: str | Element) -> None:
        sel, name = self._resolve(selector)
        self._log("click", name)
        self._page.click(sel)

    @allure_step
    def goto(self, url: str, **kwargs: Any) -> Any:
        self._log("goto", url)
        return self._page.goto(url, **kwargs)

    @allure_step
    def wait_for_selector(self, selector: str | Element, **kwargs: Any) -> ElementHandle | None:
        sel, name = self._resolve(selector)
        self._log("wait_for_selector", name, str(kwargs))
        return self._page.wait_for_selector(sel, **kwargs)

    @allure_step
    def wait_for_url(self, url: str | Any, **kwargs: Any) -> None:
        self._log("wait_for_url", str(url))
        self._page.wait_for_url(url, **kwargs)

    @allure_step
    def wait_for_load_state(self, state: Literal["domcontentloaded", "load", "networkidle"] = "load") -> None:
        self._log("wait_for_load_state", state)
        self._page.wait_for_load_state(state)

    def locator(self, selector: str) -> Locator:
        return self._page.locator(selector)

    @allure_step
    def is_visible(self, selector: str | Element, **kwargs: Any) -> bool:
        sel, name = self._resolve(selector)
        self._log("is_visible", name)
        return self._page.is_visible(sel, **kwargs)

    @allure_step
    def text_content(self, selector: str | Element) -> str | None:
        sel, name = self._resolve(selector)
        self._log("text_content", name)
        return self._page.text_content(sel)

    @allure_step
    def screenshot(self, **kwargs: Any) -> bytes:
        self._log("screenshot", "")
        return self._page.screenshot(**kwargs)

    def evaluate(self, expression: str, *args: Any) -> Any:
        return self._page.evaluate(expression, *args)

    def query_selector_all(self, selector: str) -> list[ElementHandle]:
        return self._page.query_selector_all(selector)

    @property
    def url(self) -> str:
        return self._page.url

    @property
    def title(self) -> str:
        return self._page.title()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._page, name)
