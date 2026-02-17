import pytest
import time
from playwright.sync_api import Page
from models.base_models import UserData
from models.page_object_models import CinescopeLoginPage


class TestLoginPage:
    """Класс для тестов страницы логина"""

    def test_login_by_ui(self, page: Page, registered_user: UserData):
        login_page = CinescopeLoginPage(page)
        login_page.open()

        login_page.login(registered_user.email, registered_user.password)

        login_page.wait_redirect_to_home_page()
        login_page.check_allert()
