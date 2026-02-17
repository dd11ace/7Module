from playwright.sync_api import Page, expect

from constants import (
    CINESCOPE_LOGIN_LINK,
    CINESCOPE_MAIN_LINK,
    CINESCOPE_MOVIES_LINK,
    CINESCOPE_REGISTER_LINK,
)


class CinescopeRegisterPage:
    """Класс для работы со страницей регистрации"""

    def __init__(self, page: Page):
        self.page = page
        self.url = CINESCOPE_REGISTER_LINK

        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")

        self.full_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.repeat_password_input = page.get_by_role(
            "textbox", name="Повторите пароль"
        )

        self.register_button = page.get_by_role("button", name="Зарегистрироваться")

        self.sign_button = page.get_by_role("link", name="Войти")

    def go_to_home_page(self):
        """Переход на главную страницу."""
        self.home_button.click()
        self.page.wait_for_url(CINESCOPE_MAIN_LINK)

    def go_to_all_movies(self):
        """Переход на страницу 'Все фильмы'."""
        self.all_movies_button.click()
        self.page.wait_for_url(CINESCOPE_MOVIES_LINK)

    def open(self):
        """Переход на страницу регистрации."""
        self.page.goto(self.url)

    def enter_full_name(self, full_name: str):
        """Ввод full_name"""
        self.full_name_input.fill(full_name)

    def enter_email(self, email: str):
        """Ввод email"""
        self.email_input.fill(email)

    def enter_password(self, password: str):
        """Ввод пароля"""
        self.password_input.fill(password)

    def enter_repeat_password(self, password: str):
        """Ввод подтверждения пароля"""
        self.repeat_password_input.fill(password)

    def click_register_button(self):
        """Клик по кнопке регистрации"""
        self.register_button.click()

    # Дополнительные действия
    def register(
        self, full_name: str, email: str, password: str, confirm_password: str
    ):
        """Полный процесс регистрации."""
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_repeat_password(confirm_password)
        self.click_register_button()

    def wait_redirect_to_login_page(self):
        """Переход на страницу login."""
        self.page.wait_for_url(CINESCOPE_LOGIN_LINK)
        expect(self.page).to_have_url(CINESCOPE_LOGIN_LINK)

    def check_allert(self):
        """Проверка всплывающего сообщения после редиректа"""
        notification_locator = self.page.get_by_text("Подтвердите свою почту")
        notification_locator.wait_for(state="visible")

        expect(notification_locator).to_be_visible()
        notification_locator.wait_for(state="hidden")
        expect(notification_locator).not_to_be_visible()
