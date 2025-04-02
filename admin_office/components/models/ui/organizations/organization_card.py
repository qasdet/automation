from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input


class OrganizationCard:
    """Модель страницы карточка организации"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.save_button = Button(
            page=page,
            locator="[data-testid='organization_card_save_button']",
            name='Сохранить',
        )
        self.role = DropDownList(
            page=page,
            locator="//div[@data-testid='organization_card_role']",
            name='Роль в системе',
        )
        self.close_button = Button(
            page=page,
            locator="[data-testid='organization_card_close_button']",
            name='Закрыть',
        )
        self.active_button = Button(
            page=page,
            locator="[data-testid='organization_card_active_button']",
            name='Активировать',
        )
        self.blocked_button = Button(
            page=page,
            locator="[data-testid='organization_card_block_button']",
            name='Блокировать',
        )
        self.input_okopf = Input(
            page=page,
            locator="[data-testid='organization_card_okopf']",
            name='ОКОПФ',
        )
        self.input_full_name = Input(
            page=page,
            locator="[data-testid='organization_card_full_name']",
            name='Полное название',
        )
        self.input_short_name = Input(
            page=page,
            locator="[data-testid='organization_card_short_name']",
            name='Короткое название',
        )
        self.input_firm_name = Input(
            page=page,
            locator="[data-testid='organization_card_firm_name']",
            name='Фирменное название',
        )
        self.input_address = Input(
            page=page,
            locator="[data-testid='organization_card_address']",
            name='Юр. адрес',
        )
        self.input_phone = Input(
            page=page,
            locator="[data-testid='organization_card_phone']",
            name='Телефон',
        )
        self.input_email = Input(
            page=page,
            locator="[data-testid='organization_card_email']",
            name='E-mail',
        )
        self.input_inn = Input(
            page=page,
            locator="[data-testid='organization_card_inn']",
            name='ИНН',
        )
        self.input_kpp = Input(
            page=page,
            locator="[data-testid='organization_card_kpp']",
            name='КПП',
        )
        self.input_ogrn = Input(
            page=page,
            locator="[data-testid='organization_card_ogrn']",
            name='ОГРН/ОГРНИП',
        )

    def fill_all_fields(
        self,
        data_organization: dict,
    ) -> None:
        """Заполяем все поля формы
        Args:
            data_organization: данные для организации
        """
        if data_organization['roleCode'] == 'agency':
            data_organization['roleCode'] = 'Рекламное агентство'
        else:
            data_organization['roleCode'] = 'Клиент'
        self.role.select_item_by_text(data_organization['roleCode'])
        self.input_okopf.fill(data_organization['okopf'])
        self.input_full_name.fill(data_organization['fullName'])
        self.input_short_name.fill(data_organization['shortName'])
        self.input_firm_name.fill(data_organization['firmName'])
        self.input_address.fill(data_organization['address'])
        self.input_phone.fill(data_organization['phone'])
        self.input_email.fill(data_organization['email'])
        self.input_inn.fill(data_organization['inn'])
        self.input_kpp.fill(data_organization['kpp'])
        self.input_ogrn.fill(data_organization['ogrn'])

    def save_organization(self) -> None:
        """Сохранить организацию"""
        self.save_button.click()
        self.save_button.should_be_not_visible()
