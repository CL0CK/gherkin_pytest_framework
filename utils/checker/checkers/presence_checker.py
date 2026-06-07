from playwright.sync_api import Locator
from utils.checker.dto import ElementDTO


class PresenceChecker:
    def check(self, locator: Locator, dto: ElementDTO):
        if dto.is_visible and not dto.is_hidden:
            locator.first.wait_for(state="visible", timeout=dto.timeout)
        if dto.is_hidden and not dto.is_visible:
            self._wait_hidden(locator, dto.timeout)

    def _wait_hidden(self, locator: Locator, timeout: int):
        import time
        end = time.time() + timeout / 1000
        while time.time() < end:
            try:
                count = locator.count
                if count == 0:
                    return
            except Exception:
                return
            time.sleep(0.2)
        raise TimeoutError(f"Element still visible after {timeout}ms")

    def check_visible(self, locator: Locator, timeout: int = 5000):
        locator.first.wait_for(state="visible", timeout=timeout)

    def check_hidden(self, locator: Locator, timeout: int = 5000):
        self._wait_hidden(locator, timeout)
