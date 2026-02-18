import pytest
import allure
from playwright.sync_api import Page

from models.page_object_models import CinescopeRegisterPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы Register")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("ui")
@pytest.mark.ui
class TestRegistrationPage:
    """Класс с тестами регистрации"""

    @allure.feature("Регистрация")
    @allure.story("Успешная регистрация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проведение успешной регистрации")
    @pytest.mark.critical
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_register_by_ui(
        self, page: Page, test_email: str, test_name: str, test_password: str
    ):
        random_password = test_password
        register_page = CinescopeRegisterPage(page)
        register_page.open()

        register_page.register(
            f"PlaywrightTest {test_name}",
            test_email,
            random_password,
            random_password,
        )

        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()
