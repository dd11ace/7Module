import allure
from playwright.sync_api import Page, Locator, expect


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста {text} в поле {locator}")
    def enter_text_to_element(self, locator: Locator, text: str):
        self.page.locator(locator.fill(text))

    @allure.step('Клик по элементу "{locator}"')
    def click_element(self, locator: Locator):
        self.page.locator(locator.click())

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        expect(self.page).to_have_url(url)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: Locator) -> str:
        return self.page.locator(locator).text_content()

    @allure.step(
        "Ожидание появления или исчезновения элемента: {locator}, state = {state}"
    )
    def wait_for_element(self, locator: Locator, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(
                file.read(),
                name="Screenshot after redirect",
                attachment_type=allure.attachment_type.PNG,
            )

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:

        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            notification_locator.wait_for(state="visible")
            expect(notification_locator).to_be_visible()

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            notification_locator.wait_for(state="hidden")
            expect(notification_locator).not_to_be_visible()
