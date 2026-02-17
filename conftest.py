import pytest
import requests
from playwright.sync_api import Playwright, Browser, BrowserContext
from common.tools import Tools
from constants import AUTH_URL, DEFAULT_UI_TIMEOUT, REGISTER_ENDPOINT

from enums.roles import Roles
from utils.data_generator import DataGenerator
from custom_requster.custom_requester import CustomRequester
from models.base_models import UserData


@pytest.fixture
def test_email():
    """Возвращает случайный email"""
    email = DataGenerator.generate_random_email()
    return email


@pytest.fixture
def test_name():
    """Возвращает случайное имя"""
    name = DataGenerator.generate_random_name()
    return name


@pytest.fixture
def test_password():
    """Возвращает случайный пароль"""
    password = DataGenerator.generate_random_password()
    return password


@pytest.fixture(name="test_user")
def test_user_data() -> UserData:
    """Генерация случайного пользователя для тестов."""
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return UserData(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER],
    )


@pytest.fixture(scope="session")
def requester() -> CustomRequester:
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_URL)


@pytest.fixture()
def registered_user(requester: CustomRequester, test_user: UserData) -> UserData:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    user_data = test_user.model_dump()
    response = requester.send_request(
        method="POST", endpoint=REGISTER_ENDPOINT, data=user_data, expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.model_copy()
    registered_user.id = response_data.get("id")
    return registered_user


@pytest.fixture(scope="session")
def session() -> requests.Session:
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


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
