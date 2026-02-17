import allure
from playwright.sync_api import Page, expect

from constants import CINESCOPE_MAIN_LINK, CINESCOPE_MOVIES_LINK
from models.base_action import PageAction


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = CINESCOPE_MAIN_LINK

        self.home_button = page.get_by_role("link", name="Cinescope")
        self.all_movies_button = page.get_by_role("link", name="Все фильмы")

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.home_button.click()
        self.wait_redirect_for_url(self.home_url)

    @allure.step('Переход на страницу "Все фильмы" из шапки сайта')
    def go_to_all_movies(self):
        self.all_movies_button.click()
        self.wait_redirect_for_url(CINESCOPE_MOVIES_LINK)
