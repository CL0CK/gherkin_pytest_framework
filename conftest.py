import os

import allure
from playwright.sync_api import BrowserContext, Page, sync_playwright
import pytest

from utils.config import Settings
from utils.logger import get_logger

logger = get_logger()
settings = Settings()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"browser={settings.browser}\n")
        f.write("viewport=1280x720\n")
        f.write(f"headless={settings.headless}\n")
        f.write(f"base_url={settings.base_url}\n")
        f.write("python_version=3.13\n")
        f.write("playwright_version=1.60.0\n")


@pytest.fixture(scope="session")
def playwright_instance():
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, settings.browser)
    browser_args = {
        "headless": settings.headless,
        "slow_mo": settings.slow_mo,
    }
    browser = browser_type.launch(**browser_args)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser) -> BrowserContext:
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    if settings.video_on_failure:
        ctx.tracing.start(screenshots=True, snapshots=True)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    pg = context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="function")
def config() -> Settings:
    return settings


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_obj = None
        for fixture_name in ("page",):
            if fixture_name in item.fixturenames:
                page_obj = item.funcargs.get(fixture_name)
                break

        if page_obj and settings.screenshot_on_failure:
            try:
                screenshot = page_obj.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"screenshot_{report.nodeid}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")

        try:
            log_file = f"logs/test_{report.nodeid.replace('/', '_').replace(':', '_')}.log"
            import os

            if os.path.exists(log_file):
                with open(log_file) as f:
                    allure.attach(
                        f.read(),
                        name="test_log",
                        attachment_type=allure.attachment_type.TEXT,
                    )
        except Exception as e:
            logger.error(f"Failed to attach log: {e}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    logger.info(f"▶ Environment: browser={settings.browser} | viewport=1280x720 | headless={settings.headless}")
    allure.label("browser", settings.browser)
    allure.label("viewport", "1280x720")
    allure.label("headless", str(settings.headless))
    allure.label("base_url", settings.base_url)
