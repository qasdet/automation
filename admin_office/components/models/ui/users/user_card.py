from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title


class UserCard:
    """Модель страницы карточки пользователя"""

    def __init__(self, page: Page) -> None:
        self.save_button = Button(
            page=page,
            locator="[data-testid='user_card_save_button']",
            name='Сохранить',
        )
        self.cancel_button = Button(
            page=page,
            locator="[data-testid='user_card_cancel_button']",
            name='Отмена',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='user_card_title']",
            name='Заголовок',
        )
        self.input_last_name = Input(
            page=page,
            locator="[data-testid='user_card_last_name']",
            name='Фамилия',
        )
        self.input_name = Input(
            page=page, locator="[data-testid='user_card_name']", name='Имя'
        )
        self.input_middle_name = Input(
            page=page,
            locator="[data-testid='user_card_middle_name']",
            name='Отчество',
        )
        self.input_email = Input(
            page=page, locator="[data-testid='user_card_email']", name='E-mail'
        )
        self.input_login = Input(
            page=page, locator="[data-testid='user_card_login']", name='Логин'
        )
        self.input_phone = Input(
            page=page,
            locator="[data-testid='user_card_phone']",
            name='Телефон',
        )
        self.input_contact_phone = Input(
            page=page,
            locator="[data-testid='user_card_contact_phone']",
            name='Контактный телефон',
        )
        self.role = DropDownList(
            page=page,
            locator="//div[@data-testid='user_card_role']",
            name='Роль',
        )
        self.organization = DropDownList(
            page=page,
            locator="//div[@data-testid='user_card_organization']",
            name='Оранизация',
        )

    def fill_all_fields(
        self,
        surname: str,
        name: str,
        middle_name: str,
        email: str,
        login: str,
        phone: str,
        contact_phone: str,
        role: str,
        organization: str,
    ) -> None:
        """Заполяем все поля формы
        Args:
            last_name Фамилия
            name Имя
            middle_name Отчество
            email Почта
            login Логин
            phone Телефон
            contact_phone Контактный телефон
            role Роль
            organization Организация
        """
        self.input_last_name.fill(surname)
        self.input_name.fill(name)
        self.input_middle_name.fill(middle_name)
        self.input_email.fill(email)
        self.input_login.fill(login)
        self.input_phone.fill(phone)
        self.input_contact_phone.fill(contact_phone)
        self.role.select_item_by_text(role)
        self.organization.select_item_by_text(organization)

    def save_user(self) -> None:
        """Сохранить организацию"""
        self.save_button.click()
        self.save_button.should_be_not_visible()
