from playwright.sync_api import Page
from controller.button import Button
from controller.input import Input
from controller.title import Title
from gitlab_conf import ENV_VARIABLES


class FormAuthorization:
    """Модель страницы авторизации"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.user_name = Input(
            page=page, locator="//input[@id='username']", name='username'
        )
        self.passwd = Input(
            page=page, locator="//input[@id='password']", name='password'
        )
        self.save_btn = Button(
            page=page, locator='//button[@class="btn"]', name='btn'
        )
        self.change_user = Title(
            page,
            locator='text="Сменить пользователя"',
            name='Сменить пользователя',
        )
        self.sso_login_btn = Button(
            page,
            locator='text="Войти по sso"',
            name='Войти по sso'
        )

    def input_login(self):
        self.user_name.fill(ENV_VARIABLES.get('admin_office_login'))

    def input_passwd(self):
        self.passwd.fill(ENV_VARIABLES.get('admin_office_password'))

    def enter_btn(self) -> None:
        """Нажать кнопку Войти"""
        self.save_btn.click()

    def auth_admin_office(self) -> None:
        """Метод для входа в админку.

        Если тесты запускаются локально, то необходимо раскомментировать две строчки ниже
        """
        self.sso_login_btn.should_be_visible()
        self.sso_login_btn.click()
        # self.change_user.click()
        self.user_name.should_be_visible()
        self.input_login()
        self.input_passwd()
        self.enter_btn()
