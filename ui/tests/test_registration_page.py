import pytest
import time
from playwright.sync_api import Page

from models.page_object_models import CinescopeRegisterPage


class TestRegistrationPage:
    """Класс с тестами регистрации"""

    def test_register_by_ui(
        self, page: Page, test_email: str, test_name: str, test_password: str
    ):
        random_password = test_password
        register_page = CinescopeRegisterPage(page)
        register_page.open()

        register_page.register(
            f"PlaywrightTest {test_name}", test_email, random_password, random_password
        )

        register_page.wait_redirect_to_login_page()
        register_page.check_allert()

        time.sleep(3)
