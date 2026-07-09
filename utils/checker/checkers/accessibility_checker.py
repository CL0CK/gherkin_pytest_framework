from typing import Any

from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

from utils.allure.step import CheckStep
from utils.config import Settings
from utils.element import Element, resolve_locator


class AccessibilityChecker:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._settings = Settings()

    def _locator(self, element: Element | Page) -> Any:
        # Axe can take a page or a specific selector/element
        if isinstance(element, Page):
            return element
        return resolve_locator(self._page, element)

    @CheckStep
    def check_accessibility(self, element=None) -> None:
        axe = Axe()

        # If no element is provided, scan the whole page
        target = self._page if element is None else self._locator(element)

        results = axe.run(target)
        # AxeResults object stores violations in the .violations attribute
        violations = results.violations if hasattr(results, 'violations') else []

        if not violations:
            return

        # Filter by fail level from config
        fail_level = self._settings.a11y_fail_level
        level_priority = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
        min_priority = level_priority.get(fail_level, 1)

        # Refined filter: only fail if the violation's impact is within our threshold
        relevant_violations = []
        for v in violations:
            impact = v.get("impact", "minor")
            if level_priority.get(impact, 9) <= min_priority:
                relevant_violations.append(v)

        if relevant_violations:
            error_msg = "\n".join([f"- {v['id']}: {v['help']} (Impact: {v['impact']})" for v in relevant_violations])
            print(f"\n--- Accessibility Report ---\n{error_msg}\n--------------------------")
            raise AssertionError(f"Accessibility violations found at level {fail_level} or higher:\n{error_msg}")
