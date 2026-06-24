from collections.abc import Callable
import functools
import time

from utils.logger import get_logger

logger = get_logger()


def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{retries} failed for {func.__name__}: {e}")
                    if attempt < retries:
                        time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


def assert_element_visible(page, selector, timeout: int = 5000):
    page.wait_for_selector(selector, state="visible", timeout=timeout)


def assert_element_hidden(page, selector, timeout: int = 5000):
    page.wait_for_selector(selector, state="hidden", timeout=timeout)


def assert_text_contains(page, selector, expected_text, timeout: int = 5000):
    element = page.wait_for_selector(selector, timeout=timeout)
    actual_text = element.inner_text()
    assert expected_text in actual_text, f"Expected '{expected_text}' in '{actual_text}', but not found"


def assert_url_matches(page, expected_path: str, timeout: int = 5000):
    page.wait_for_url(lambda url: expected_path in url, timeout=timeout)


def assert_text_equals(page, selector, expected_text, timeout: int = 5000):
    element = page.wait_for_selector(selector, timeout=timeout)
    actual_text = element.inner_text()
    assert actual_text == expected_text, f"Expected '{expected_text}', got '{actual_text}'"
