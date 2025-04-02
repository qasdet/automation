import re

from playwright.sync_api import Page
from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title
from modals.dialog_modal import DialogModal
from user_office.constants import PATTERN_ID


class UserCard:
    """Карточка пользователя в user office (создание, редактирование)"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.confirmation_dialog = DialogModal(page)
        self.title = Title(
            page=page,
            locator='h2',
            name='Заголовок',
        )
        self.status = Title(
            page=page,
            locator='h2 span',
            name='Статус',
        )
        self.surname = Input(
            page=page,
            locator="[name='surname']",
            name='Фамилия',
        )
        self.name = Input(
            page=page,
            locator="[name='name']",
            name='Имя',
        )
        self.middle_name = Input(
            page=page,
            locator="[name='middleName']",
            name='Отчество',
        )
        self.login = Input(
            page=page,
            locator="[name='login']",
            name='Логин',
        )
        self.phone = Input(
            page=page,
            locator="[name='phone']",
            name='Телефон',
        )
        self.contact_phone = Input(
            page=page,
            locator="[name='contactPhone']",
            name='Контактный телефон',
        )
        self.email = Input(
            page=page,
            locator="[name='email']",
            name='Электронная почта',
        )
        self.role = DropDownList(
            page=page,
            locator="[id='rolesID']",
            name='Роль',
        )
        self.cancel_btn = Button(
            page=page,
            locator="//button[.='Отмена']",
            name='Отмена',
        )
        self.save_btn = Button(
            page=page,
            locator="//button[.='Сохранить']",
            name='Сохранить',
        )
        self.blocked_btn = Button(
            page=page,
            locator="//button[.='Заблокировать']",
            name='Заблокировать',
        )

    def fill_all_fields(self, **kwargs) -> None:
        """Заполняем все поля формы"""
        self.surname.fill(kwargs['surname'])
        self.name.fill(kwargs['name'])
        self.middle_name.fill(kwargs['middle_name'])
        self.login.click()
        self.login.fill(kwargs['login'])
        self.phone.click()
        self.phone.fill(kwargs['phone'])
        self.contact_phone.click()
        self.contact_phone.fill(kwargs['contact_phone'])
        self.email.fill(kwargs['email'])
        if self.role.get_locator().text_content() != kwargs['role']:
            self.role.select_item_by_text(kwargs['role'])

    def save_user(self) -> None:
        """Сохранить пользователя"""
        self.save_btn.click()
        self.save_btn.should_be_not_visible()

    def check_the_card_is_visible(self) -> None:
        """Проверить, что карточка пользователя отображается"""
        self.save_btn.should_be_visible()

    def check_user_info(self, **kwargs) -> None:
        """Проверить, что данные пользователя в карточке совпадают с ожидаемыми"""
        self.status.should_have_text(kwargs['status'])
        self.surname.should_have_value(kwargs['surname'])
        self.name.should_have_value(kwargs['name'])
        self.middle_name.should_have_value(kwargs['middle_name'])
        self.login.should_have_value(kwargs['login'])
        self.phone.should_have_value(
            f"+7 {kwargs['phone'][:3]} {kwargs['phone'][3:6]} {kwargs['phone'][6:8]} {kwargs['phone'][8:]}"
        )
        self.contact_phone.should_have_value(f"+7 {kwargs['contact_phone']}")
        self.email.should_have_value(kwargs['email'])
        self.role.should_have_text(kwargs['role'])

    def blocked_user(self) -> None:
        """Заблокировать пользователя"""
        self.blocked_btn.click()
        self.confirmation_dialog.confirm()

    def get_user_id(self) -> str:
        """Получить id пользователя из url"""
        pattern = re.compile(PATTERN_ID)
        user_id = pattern.findall(self.page.url)
        if len(user_id) > 0:
            return user_id[0]
        else:
            raise Exception('id пользователя не найден')
