from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Locator, Page


class Element:
    def __init__(self, selector: str, name: str = "", page: Page | None = None) -> None:
        self.selector = selector
        self._name = name
        self.page = page

    @property
    def name(self) -> str:
        return self._name or self.selector

    def locator(self) -> Locator:
        if self.page is None:
            raise ValueError(f"Page not set for Element '{self.name}'. Did you forget to call BasePage.__init__?")
        return self.page.locator(self.selector)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Element({self.selector!r}, name={self._name!r})"
