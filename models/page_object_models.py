import allure
import pytest
from playwright.sync_api import Page

from constants import (
    CINESCOPE_LOGIN_LINK,
    CINESCOPE_REGISTER_LINK,
)
from models.base_page import BasePage


@allure.epic("Регистрация")
@allure.feature("Страница регистрации")
@allure.tag("ui")
@pytest.mark.ui
class CinescopeRegisterPage(BasePage):
    """Класс для работы со страницей регистрации"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = CINESCOPE_REGISTER_LINK

        self.full_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.repeat_password_input = page.get_by_role(
            "textbox", name="Повторите пароль"
        )

        self.register_button = page.get_by_role("button", name="Зарегистрироваться")

        self.sign_button = page.get_by_role("link", name="Войти")

    def open(self):
        """Переход на страницу регистрации."""
        self.page.goto(self.url)

    def register(
        self, full_name: str, email: str, password: str, confirm_password: str
    ):
        """Полный процесс регистрации."""
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, confirm_password)

        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(CINESCOPE_LOGIN_LINK)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


@allure.epic("Авторизация")
@allure.feature("Страница авторизации")
@allure.tag("ui")
@pytest.mark.ui
class CinescopeLoginPage(BasePage):
    """Класс для работы со страницей логина"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = CINESCOPE_LOGIN_LINK

        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль")

        self.login_button = page.locator("form").get_by_role("button", name="Войти")

        self.register_link = page.get_by_role("link", name="Зарегистрироваться")

    def open(self):
        """Переход на страницу регистрации."""
        self.page.goto(self.url)

    def login(self, email: str, password: str):
        """Полный процесс входа"""
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")
