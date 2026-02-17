import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext
from common.tools import Tools
from constants import DEFAULT_UI_TIMEOUT


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir("playwright_trace", log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture()
def page(context: BrowserContext):
    page = context.new_page()
    yield page
    page.close()
