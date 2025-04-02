import allure
import pytest

from allure import attachment_type
from playwright.sync_api import Page, sync_playwright
from gitlab_conf import ENV_VARIABLES, get_env_variables

pytest_plugins = ['helper.fixtures']


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args) -> dict[str, bool]:
    return {**browser_context_args, 'ignore_https_errors': True}


def pytest_addoption(parser) -> None:
    parser.addoption('--stand', default='DEV')


@pytest.fixture(scope='session', autouse=True)
def set_env_variables(request) -> None:
    """Получение переменных окружения
    Примечание: фикстура запускается без вызова один раз при запуске тестов.
    Значения переменных хранятся в словаре ENV_VARIABLES
    """
    test_stand = request.config.getoption('--stand')
    get_env_variables(test_stand)


@pytest.fixture(scope='session')
def admin_base_url() -> str | None:
    return ENV_VARIABLES.get('admin_office_url')


@pytest.fixture(scope='session')
def office_base_url() -> str | None:
    return ENV_VARIABLES.get('user_office_url')

@pytest.fixture(scope='session')
def yandex_login() -> str | None:
    return ENV_VARIABLES.get('yandex_login')

@pytest.fixture(scope='session')
def yandex_password() -> str | None:
    return ENV_VARIABLES.get('yandex_password')

@pytest.fixture(scope='session')
def landing_base_url() -> str | None:
    return ENV_VARIABLES.get('landing_url')


@pytest.fixture(scope='session')
def graphql_url() -> str | None:
    return ENV_VARIABLES.get('graphql_url')


@pytest.fixture(scope='session')
def admin_api_auth_url() -> str | None:
    return ENV_VARIABLES.get('admin_api_auth_url')


@pytest.fixture(scope='session')
def user_office_gateway_auth_url() -> str | None:
    return ENV_VARIABLES.get('user_office_gateway_auth_url')


# TODO: позже добавлю переключатель режимов - инкогнито и обычный режим
@pytest.fixture(scope='module')
def chromium_page():
    """для переключения режима достаточно сменить флаг
    :config - False - инкогнито
    :config - True обычный режим
    :head True/False- переключение headless режима
    """
    config = False
    head = False
    match config | head:
        case True:
            with sync_playwright() as playwright:
                chromium = playwright.chromium.launch_persistent_context(
                    permissions=['clipboard-read', 'clipboard-write'],
                    user_data_dir='',
                    headless=head,
                    slow_mo=600,
                    ignore_https_errors=True,
                    viewport={'width': 1920, 'height': 1080},
                )
                yield chromium.new_page()
        case False:
            with sync_playwright() as playwright:
                chromium = playwright.chromium.launch(
                    headless=head,
                    slow_mo=600,
                ).new_context(
                    permissions=['clipboard-read', 'clipboard-write'],
                    ignore_https_errors=True,
                    viewport={'width': 1920, 'height': 1080},
                )
                yield chromium.new_page()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    loc = rep.location[0]
    if rep.when == "call" and rep.failed:
        screenshot_file = f"screenshots/{item.name}.png"
        item.funcargs["chromium_page"].screenshot(path=screenshot_file)
        allure.attach.file(source=screenshot_file, name="FailedTest", attachment_type=attachment_type.PNG)
    elif loc[:29] == 'user_office\\tests\\digital\\api':
        pass
    elif loc[:23] == 'admin\\tests\\digital\\api\\':
        pass
