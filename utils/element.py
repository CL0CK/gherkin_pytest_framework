from playwright.sync_api import Locator, Page


class Element:
    def __init__(self, selector: str, name: str = "") -> None:
        self.selector = selector
        self._name = name

    @property
    def name(self) -> str:
        return self._name or self.selector

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Element({self.selector!r}, name={self._name!r})"


def resolve_locator(page: Page, target: "Element | Locator") -> Locator:
    """
    Resolves a checker target to a Playwright Locator.

    - An Element resolves against the full page (page.locator(element.selector)),
      same as before — fine for page-level elements with no ambiguity.
    - A Locator (e.g. one already scoped to a Component Object's root, like
      product_card.locator(ProductCard.ADD_TO_CART_BUTTON)) is passed through
      unchanged, preserving whatever scoping the caller already set up.

    Without this, checker.* calls always re-resolved against the whole page,
    silently discarding any Component Object scoping — harmless with exactly
    one matching element on the page, wrong (or a Playwright strict-mode
    error) the moment there are two or more.
    """
    if isinstance(target, Locator):
        return target
    return page.locator(target.selector)
