from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input


class LandingGeneral:
    """Модель посадочной страницы"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.leave_a_request_button_first = Button(
            page,
            locator="[data-testid='request_button_to_form']",
            name='Оставить заявку',
        )
        self.leave_a_request_button_second = Button(
            page,
            locator="[data-testid='send_a_request']",
            name='Оставить заявку',
        )
        self.name = Input(page, locator="[data-testid='name']", name='Имя*')
        self.second_name = Input(
            page, locator="[data-testid='second_name']", name='Фамилия*'
        )
        self.email = Input(
            page, locator="[data-testid='email']", name='Электронная почта*'
        )
        self.organization_name = Input(
            page,
            locator="[data-testid='organization_name']",
            name='Название вашей организации*',
        )
        self.phone_number = Input(
            page,
            locator="[data-testid='phone-number']",
            name='Номер телефона*',
        )
        self.organization_role_dropdown = DropDownList(
            page,
            locator="[data-testid='organization_role']",
            name='Роль организации*',
        )
        self.organization_role_field = Input(
            page,
            locator='#react-select-role-input',
            name='Роль организации*',
        )
        self.comments = Input(
            page, locator="[data-testid='comment']", name='Комментарии'
        )

    def click_leave_a_first_request_button(self) -> None:
        """Нажатие на кнопку отправки формы"""
        self.leave_a_request_button_first.should_be_visible()
        self.leave_a_request_button_first.click()

    def click_leave_a_second_request_button(self) -> None:
        """Нажатие на кнопку отправки формы"""
        self.leave_a_request_button_second.should_be_visible()
        self.leave_a_request_button_second.click()

    def fill_the_name(self, name_field_value) -> None:
        """Заполнить поле 'Имя'"""
        self.name.should_be_visible()
        self.name.fill(name_field_value)

    def fill_the_second_name(self, second_name_field_value) -> None:
        """Заполнить поле 'Фамилия'"""
        self.second_name.should_be_visible()
        self.second_name.fill(second_name_field_value)

    def fill_the_email(self, email_field_value) -> None:
        """Заполнить поле 'Электронная почта'"""
        self.email.should_be_visible()
        self.email.fill(email_field_value)

    def fill_the_phone(self, phone_number_field_value) -> None:
        """Заполнить поле 'Номер телефона'"""
        self.phone_number.should_be_visible()
        self.phone_number.fill(phone_number_field_value)

    def fill_the_organization_name(
        self, organization_name_field_value
    ) -> None:
        """Заполнить поле 'Название вашей организации'"""
        self.organization_name.should_be_visible()
        self.organization_name.fill(organization_name_field_value)

    def click_choose_organization_role(self, organization_role_field_value):
        self.organization_role_dropdown.click()
        self.organization_role_field.fill(organization_role_field_value)
        self.organization_role_dropdown.page.keyboard.press('Enter')

    def fill_the_comments(self, comments_field_value) -> None:
        """Заполнить поле 'Комментарии'"""
        self.comments.should_be_visible()
        self.comments.fill(comments_field_value)

    def input_all_landing_fields(self, **data_to_fill) -> None:
        """Заполняет поля посадочной страницы"""
        self.fill_the_second_name(data_to_fill['surname'])
        self.fill_the_email(data_to_fill['email'])
        self.fill_the_phone(data_to_fill['phone'])
        self.fill_the_organization_name(data_to_fill['firm_name'])
        self.fill_the_comments(data_to_fill['comments'])
        self.click_choose_organization_role(data_to_fill['role'])
        self.fill_the_name(data_to_fill['name'])
