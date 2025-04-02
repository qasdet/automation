from playwright.sync_api import Page

from controller.button import Button
from controller.input import Input
from gitlab_conf import ENV_VARIABLES


class AuthorizeUserOffice:
    """Модель страницы авторизации в user office"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.email = Input(page, locator="//input[@id='email']", name='email')
        self.phone = Input(page, locator="//input[@id='login']", name='login')
        self.password = Input(
            page, locator="//input[@id='password']", name='IDToken2'
        )
        self.save_button = Button(
            page, locator="[type='submit']", name='Далее'
        )

    def input_email(self):
        # Логин добавлен в данном виде временно
        self.email.fill(
            ENV_VARIABLES.get('user_office_login'), validate_value=True
        )

    def input_phone(self):
        # Логин добавлен в данном виде временно
        self.phone.fill('asgalkin2@mts.ru', validate_value=True)

    def input_password(self):
        # Пароль в данном добавлен виде временно
        self.password.fill(
            ENV_VARIABLES.get('user_office_password'), validate_value=False
        )

    def auth_user_office(self):
        # self.input_phone()
        self.input_email()
        self.save_button.click()
        self.input_password()
        self.save_button.click()
