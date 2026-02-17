import pytest
import allure
import time
from playwright.sync_api import Page
from models.base_models import UserData
from models.page_object_models import CinescopeLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы login")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("ui")
@pytest.mark.ui
class TestLoginPage:
    """Класс для тестов страницы логина"""

    @allure.feature("Вход в систему")
    @allure.story("Успешный вход в систему")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проведение успешного входа в систему")
    @pytest.mark.critical
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_by_ui(self, page: Page, registered_user: UserData):
        login_page = CinescopeLoginPage(page)
        login_page.open()

        login_page.login(registered_user.email, registered_user.password)

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_allert_was_pop_up()

        time.sleep(3)
