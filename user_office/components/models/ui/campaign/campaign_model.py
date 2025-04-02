import unittest

from datetime import date
from playwright.sync_api import Page, expect
from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.list_item import ListItem
from controller.table_new import Table
from controller.title import Title
from controller.link import Link
from controller.context_menu import ContextMenu
from db_stuff.db_interactions.widget_mplan_unique_number_db_interactions import widget_in_mplan_unique_number
from helper.default_dates import (
    get_default_campaign_begin_date_for_ui,
    get_default_campaign_end_date_for_ui,
)
from helper.metric_calculator import MetricsCalculator
from user_office import constants
from user_office.components.models.ui.filter_campaign.filter import Filter
from db_stuff.db_interactions.brands_db_interactions import get_brand_name_by_id
from db_stuff.db_interactions.products_db_interactions import get_product_name_by_id


class DigitalCampaign(unittest.TestCase):
    """Модель страницы карточки digital кампании"""

    def __init__(self, page: Page) -> None:
        super().__init__()
        self.page = page
        self.table = Table(page, locator='//table', name='Таблица медиапланов')
        self.first_notification_close_button = Button(
            page=page,
            locator="text='Понятно'",
            name='Понятно',
        )
        self.campaign_goal = Title(
            page=page,
            locator="#marketTarget div",
            name='Цель кампании'
        )
        self.campaign_status = Title(
            page, locator='data-testid=campaign_status', name='Статус кампании'
        )
        self.campaign_information = Title(
            page,
            locator='data-testid=campaign_information',
            name='Нейминг и дата создания кампании',
        )
        self.campaign_period = Title(
            page,
            locator='data-testid=campaign_period',
            name='Период действия кампании',
        )
        self.campaign_type = Title(
            page, locator='data-testid=campaign_type', name='Тип кампании'
        )
        self.campaign_client = Title(
            page, locator='data-testid=campaign_client', name='Клиент'
        )
        self.campaign_product_and_brand = Title(
            page,
            locator='data-testid=campaign_brands_and_products',
            name='Продукт-бренд кампании',
        )
        self.campaign_co_brand = Title(
            page,
            locator='data-testid=campaign_cobrands',
            name='Ко-бренд кампании',
        )
        self.digital_link = Button(
            page, locator="text='Диджитал'", name='Диджитал'
        )
        self.campaign_name = Title(
            page,
            locator='data-testid=campaign_title',
            name='Название кампании',
        )
        self.campaign_code_and_create_date = Title(
            page,
            locator='data-testid=campaign_information',
            name='Код и ' 'дата ' 'создания',
        )
        self.menu_actions = Button(
            page,
            locator='data-testid=campaign_menu_actions',
            name='Меню действий',
        )
        self.retry_button = Button(
            page, locator="text='Повторить'", name='Повторить'
        )
        self.mediaplan_button = Button(
            page=page,
            locator="[data-testid='campaign_widget_view_button']",
            name='Кнопка перехода на страницу медиаплана',
        )
        self.about_campaign = Button(
            page=page,
            locator="[data-testid='campaign_about']",
            name='Кнопка перехода к просмотру кампании',
        )
        self.context_menu = Button(
            page=page,
            locator="[data-testid='campaign_menu_actions']",
            name='Кнопка контекстного меню на странице кампании',
        )
        self.context_menu_actions = Button(
            page=page,
            locator="[data-testid='campaign_actions']",
            name='Действие в контестном меню',
        )
        self.create_mediaplan_btn = Button(
            page=page,
            locator="[data-testid='digital-media-plan-create']",
            name='Кнопка перехода на страницу создания медиаплана',
        )
        self.campaign_thermometer = Title(
            page=page,
            locator="[data-testid='campaign_thermometer']",
            name='Шкала заполнения-Градусник'
        )
        self.campaign_widget_setting_placements = Title(
            page=page,
            locator="[data-testid='campaign_widget_setting_placements']",
            name='Виджет настроек размещения'
        )
        self.campaign_widget_publish_placements = Title(
            page=page,
            locator="[data-testid='campaign_widget_publish_placements']",
            name="Виджет"
        )
        self.mediaplan_title = Title(
            page=page,
            locator="[data-testid='campaign_widget_mplan_title']",
            name="Медиаплан"
        )
        self.plan_fact = Title(
            page=page,
            locator='text="Отчет план-факт"',
            name='Отчет план-факт'
        )
        self.connected = Title(
            page=page,
            locator='text="Подключения"',
            name='Подключения'
        )
        self.platform = Title(
            page=page,
            locator='text="Площадки"',
            name='Площадки'
        )
        self.post_click = Title(
            page=page,
            locator='text="Post-click tool"',
            name='Post-click tool'
        )
        self.verify_tool = Title(
            page=page,
            locator='text="Verification tool"',
            name='Verification tool'
        )
        self.tracker_tool = Title(
            page=page,
            locator='text="Tracker tool"',
            name='Tracker tool'
        )
        self.one_more_co_brand = Button(
            page=page,
            locator='text="И ещё 1"',
            name='Кнопка раскрытия второго ко бренда'
        )
        self.co_brands = Title(
            page=page,
            locator="[data-testid='campaign_cobrands']",
            name='Информация о ко брендах'
        )
        self.download_template_link = Link(
            page=page,
            locator="text='шаблон'",
            name="Шаблон"
        )

    def click_download_xls_template_link(self) -> str | None:
        """Находит и нажимает ссылку 'шаблон'"""
        self.download_template_link.should_be_visible()
        with self.page.expect_download() as download_info:
            # Запускает процесс скачивания
            self.download_template_link.click()
        return download_info.value.save_as(constants.SIMPLE_MPLAN_XLS_EXPORT)

    # TODO: требуется переработка валидации виджетов на странице медиплана Done https://jira.mts.ru/browse/MDP-5826
    # TODO: дата атрибуты для виджетов https://jira.mts.ru/browse/MDP-5832
    def check_published_campaign_page_ui(self) -> None:
        self.about_campaign.hover()
        self.about_campaign.matching_by_text(text='Подробнее о кампании')
        self.mediaplan_title.hover()
        text = self.page.get_by_test_id('campaign_widget_mplan_title').inner_text()
        self.assertEqual(first=text[:9], second='Медиаплан', msg=f'Заголовок {text} не найден')
        self.campaign_thermometer.hover()
        self.campaign_name.hover()
        self.campaign_name.should_be_visible()
        self.connected.hover()
        self.campaign_status.hover()
        self.campaign_status.has_texts(constants.APPROVED_STATUS)
        self.connected.has_texts(text='Подключения')
        self.platform.hover()
        self.platform.has_texts(text='Площадки')
        self.post_click.hover()
        self.post_click.has_texts(text='Post-click tool')
        self.verify_tool.hover()
        self.verify_tool.has_texts(text='Verification tool')
        self.tracker_tool.hover()
        self.tracker_tool.has_texts(text='Tracker tool')
        self.campaign_thermometer.should_be_visible()
        self.campaign_widget_setting_placements.hover()
        self.campaign_widget_setting_placements.should_be_visible()
        self.campaign_widget_setting_placements.has_texts(text='Отличная работа! Все размещения настроены')
        self.campaign_widget_publish_placements.hover()
        self.campaign_widget_publish_placements.should_be_visible()
        widget_placement = self.page.get_by_test_id('campaign_widget_publish_placements').inner_text()
        self.assertEqual(first=widget_placement[:-5], second='В рамках кампании осталось опубликовать размещений',
                         msg=f'Заголовок {widget_placement} не найден')

    def check_number_order_no_in_mplan_widget(self, mplan_id):
        widget = widget_in_mplan_unique_number(mplan_id)
        text = self.page.get_by_test_id('campaign_widget_mplan_title').inner_text()
        widget == text[11:]
        self.assertEqual(first=text[11:], second=widget,
                         msg=f'Уникальный номер {widget} не соответствует отображаемому')

    def open_about_campaign(self) -> None:
        """Открыть страницу просмотра кампании"""
        self.about_campaign.click()

    def open_digital_campaigns_list(self) -> None:
        """Переход на страницу списка digital кампаний"""
        self.digital_link.should_be_visible()
        self.digital_link.hover()
        self.digital_link.click()

    def open_mediaplan(self) -> None:
        """Переход на страницу медиаплана"""
        self.mediaplan_button.should_be_visible()
        self.mediaplan_button.click()

    def open_reporting_page(self) -> None:
        """Переход на страницу отчета план-факт"""
        self.page.get_by_role('button', name='Посмотреть').nth(1).click()

    def open_create_mediaplan_page(self) -> None:
        """Перейти на страницу создания медиаплана"""
        self.create_mediaplan_btn.hover()
        self.create_mediaplan_btn.should_be_visible()
        self.create_mediaplan_btn.click()

    def retry_mediaplan(self, number_row) -> None:
        """Перейти к странице повтора(создания) медиаплана
        Args:
            number_row номер строки в списке медиапланов начиная с 0
        """
        # временное решение, будет исправлено после доработки https://jira.mts.ru/browse/MDP-4977
        self.table.cell_with_number_in_row(
            number_row=number_row, number_cell=6
        ).click()
        self.table.click_item_menu_action(text_item='Повторить')

    def close_first_mp_notification(self) -> None:
        """Закрыть подсказку после создания первого медиаплана"""
        self.first_notification_close_button.click()

    def check_created_campaign_in_campaign_page(
            self, digital_test_data: dict
    ) -> None:
        """Проверка созданной кампании на основной странице. Поля заполнены
            Args:
                digital_test_data: массив тестовых данных
        """
        self.campaign_name.should_have_text(digital_test_data['campaign_name'])
        self.campaign_status.should_have_text(constants.PLANNING_STATUS)
        self.campaign_information.should_have_text(
            f'Кампания {digital_test_data["campaign_naming"]} |'
            f' Создана {date.today().strftime("%d.%m.20%y")}'
        )
        self.campaign_period.should_have_text(
            get_default_campaign_begin_date_for_ui()
            + ' - '
            + get_default_campaign_end_date_for_ui()
        )
        self.campaign_type.should_have_text(constants.DIGITAL_TYPE)
        self.campaign_client.should_have_text(constants.DIGITAL_CLIENT_NAME)
        self.campaign_product_and_brand.should_have_text(
            f'Продукт - Бренд{constants.DIGITAL_PRODUCT_NAME} - '
            f'{constants.DIGITAL_BRAND_NAME}'
        )

    def check_created_campaign_from_excel_template_import_campaign_page(
            self, cell_title
    ) -> None:
        """Проверка созданной кампании на основной странице. Поля заполнены
            Args:
                digital_test_data: массив тестовых данных
        """
        self.first_notification_close_button.click()
        self.campaign_name.should_have_text(cell_title[1][0][0])
        self.campaign_period.should_have_text(cell_title[5][0][0])
        self.campaign_client.should_have_text(cell_title[0][0][0])
        self.about_campaign.click()
        goals = self.page.locator(self.campaign_goal).first.is_visible()
        assert goals == True

    def check_new_mediaplan_planning_status(self) -> None:
        """Проверка создания медиаплана на странице кампании. Статус Планирование"""
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=2, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=3, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text=constants.PLANNING_MP_STATUS, number_cell=5, number_row=0
        )

    def check_mediaplan_draft_status(self) -> None:
        """Проверка создания медиаплана на странице кампании. Статус Черновик"""
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=2, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=3, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text='Черновик', number_cell=5, number_row=0
        )

    def check_approved_campaign_status(self) -> None:
        """Проверка статуса утверждения кампании"""
        self.campaign_status.should_have_text(constants.APPROVED_STATUS)

    def check_retried_mediaplan(self) -> None:
        """Проверка повтора медиаплана. Статус Планирование"""
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=2, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=3, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text=constants.PLANNING_MP_STATUS, number_cell=5, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=2, number_row=1
        )
        self.table.should_have_text_cell_in_row(
            check_text='—', number_cell=3, number_row=1
        )
        self.table.should_have_text_cell_in_row(
            check_text=constants.PLANNING_MP_STATUS, number_cell=5, number_row=1
        )

    def check_co_brands_in_campaign_page(self, digital_test_data: dict) -> True | False:
        """Проверка наличия ко брендов на странице кампании
            Args:
                digital_test_data: массив тестовых данных
        """
        first_co_brand_name = get_brand_name_by_id(digital_test_data['co_brand_id'])
        second_co_brand_name = get_brand_name_by_id(digital_test_data['second_co_brand_id'])
        self.one_more_co_brand.click()
        self.co_brands.should_have_text(f'Ко-бренд{first_co_brand_name + second_co_brand_name}Cвернуть  ')


class DigitalCampaignsList:
    """Модель страницы списка digital кампаний"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.strat_plans_tab = Button(
            page,
            locator="//a[.='Стратегические планы']",
            name='Стратегические планы',
        )
        self.digital_campaigns_tab = Button(
            page, locator="//a[.='Digital кампании']", name='Digital кампании'
        )
        self.tv_campaigns_tab = Button(
            page, locator="//a[.='ТВ кампании']", name='ТВ кампании'
        )
        self.filter_user_office = Filter(page)
        self.filter_button = Button(
            page,
            locator="[data-testid='campaigns_filter_button']",
            name='Кнопка фильтра списка кампаний'
        )
        self.campaigns_list_search = Button(
            page,
            locator="[data-testid='campaigns_filter_search']",
            name='Поле поиска кампаний'
        )
        self.create_campaign_button = Button(
            page,
            locator="[data-testid='campaigns_digital_create_button']",
            name='Создать кампанию',
        )
        self.table = Table(page, locator='//table', name='Таблица кампаний')
        self.column_header = Title(
            page,
            locator="//th[.='{text}']",
            name='Заголовок колонки списка кампаний. text: текст заголовка'
        )
        self.next_page_pagination = Button(
            page,
            locator="[data-testid='campaigns_digital_pagination_next']",
            name='Кнопка пагинации. Следующая страница'
        )
        self.context_menu = ContextMenu(
            page,
            locator="[data-testid='campaigns-digital-menu']",
            name='Контекстное меню'
        )
        self.context_menu_item = Button(
            page,
            locator="//button[name='{text}']",
            name='Элемент контекстного меню'
        )
        # TODO: Доработать модель контекстного меню в папке controller https://jira.mts.ru/browse/MDP-6224

    def wait_for_campaigns_page(self) -> None:
        """Ожидание прогрузки страницы digital кампаний"""
        self.page.wait_for_url('**/campaigns/digital')

    def click_strat_plans_tab(self) -> None:
        """Открыть вкладку Стратегические планы"""
        self.strat_plans_tab.should_be_visible()
        self.strat_plans_tab.click()

    def click_digital_campaign_tab(self) -> None:
        """Открыть вкладку Digital"""
        self.digital_campaigns_tab.should_be_visible()
        self.digital_campaigns_tab.click()

    def click_create_campaign_button(self) -> None:
        """Перейти на страницу создания кампании"""
        self.wait_for_campaigns_page()
        self.create_campaign_button.should_be_visible()
        self.create_campaign_button.hover()
        self.create_campaign_button.click()

    def open_campaign(self, campaign_name: str) -> None:
        """Метод для перехода на страницу кампании
        Args:
            data_campaign данные о кампании
        """
        self.table.cell_by_text(campaign_name).click()

    def retry_campaign(self, naming: str):
        """Повторение кампании"""
        self.wait_for_campaigns_page()
        self.page.get_by_role(
            'row', exact=False, name=f'{naming}'
        ).get_by_test_id('campaigns-digital-menu').click()
        self.table.click_item_menu_action(text_item='Повторить')

    def check_campaigns_list_elements(self) -> None:
        """Проверка основных элементов страницы сиска кампаний"""
        self.filter_button.should_be_visible()
        self.campaigns_list_search.should_be_visible()
        self.create_campaign_button.should_be_visible()
        # проверка заголовков списка кампаний
        column_headers = ['#', 'Медиа', 'Кампания', 'Клиент', 'Продукт, бренд и ко-бренд', 'Дата изменения', 'Статус']
        for i in column_headers:
            self.column_header.should_be_visible(text=i)
        # проверка контекстного меню и его элементов
        # TODO: Доработать модель контекстного меню в папке controller https://jira.mts.ru/browse/MDP-6224
        expect(self.table.row_with_number(0).locator(f'{self.context_menu.locator}')).to_be_visible()
        self.table.row_with_number(0).locator(f'{self.context_menu.locator}').click()
        expect(self.page.get_by_role("button", name="Открыть")).to_be_visible()
        expect(self.page.get_by_role("button", name="Повторить")).to_be_visible()
        expect(self.page.get_by_role("button", name="Отменить")).to_be_visible()
        expect(self.page.get_by_role("button", name="Удалить")).to_be_visible()

    def check_campaigns_list(self, campaigns_data: list) -> None:
        """Метод проверяет каждую запись каждой страницы списка кампаний
            Args:
                campaigns_data: массив данных списка кампаний
        """
        current_row = 0
        for i, page in enumerate(campaigns_data):
            for row in page:
                for cell_number, cell_data in enumerate(row):
                    self.table.should_have_text_cell_in_row(
                        check_text=cell_data, number_cell=cell_number, number_row=current_row
                    )
                current_row += 1
                if current_row == 10:
                    expect(self.table.row_with_number(number_row=current_row)).not_to_be_visible()
                    current_row = 0
                    if i < len(campaigns_data):
                        self.next_page_pagination.click()

    def check_created_campaign_with_two_co_brands_in_campaign_list(self, digital_test_data: dict) -> True | False:
        """Проверка отображения ко брендов созданной кампании в списке кампаний
            Args:
                digital_test_data: массив тестовых данных
        """
        brand_name = get_brand_name_by_id(digital_test_data['brand_id'])
        first_co_brand_name = get_brand_name_by_id(digital_test_data['co_brand_id'])
        product_name = get_product_name_by_id(digital_test_data['product_id'])
        self.table.should_have_text_cell_in_row(
            number_row=0, number_cell=4,
            check_text=product_name + ' - ' + brand_name + first_co_brand_name + ', +1'
        )


class DigitalCreateCampaign:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.create_camp_page = Title(
            page, locator='main', name='Страница создания кампании'
        )
        self.campaign_name = Input(
            page,
            locator="[data-testid='create_digital_campaigns_name']",
            name='Название кампании',
        )
        self.naming = Input(
            page,
            locator='data-testid=create_digital_campaigns_naming',
            name='Нейминг кампании',
        )
        self.client = DropDownList(
            page, 'data-testid=create_digital_campaigns_client', 'Клиент'
        )
        self.client_item = ListItem(
            page, locator="text='Autotest Client'", name='Autotest Client'
        )
        self.agency = DropDownList(
            page,
            locator='data-testid=create_digital_campaigns_agency',
            name='Агенство',
        )
        self.department = DropDownList(
            page,
            locator='data-testid=create_digital_campaigns_department',
            name='Подразделение',
        )
        self.agency_item = ListItem(
            page, locator='text=Autotest Agency AUTOTESTA', name='Autotest Agency AUTOTESTA'
        )
        self.brand = DropDownList(
            page,
            locator='data-testid=create_digital_campaigns_brand',
            name='Бренд',
        )
        self.product = DropDownList(
            page, 'data-testid=create_digital_campaigns_product', 'Продукт'
        )
        self.product_item = ListItem(
            page,
            locator='text=Autotest Product AUTOTESTP',
            name='Autotest Product',
        )
        self.save_draft = Button(
            page,
            locator='data-testid=create_digital_campaigns_draft_save',
            name='Создать черновик',
        )
        self.save_campaign = Button(
            page,
            locator='data-testid=create_digital_campaigns_campany_save',
            name='Создать кампанию',
        )
        self.campaign_begin = Input(
            page, locator="input[name='startOn']", name='datenow'
        )
        self.campaign_end = Input(
            page, locator="input[name='finishOn']", name='dateend'
        )
        self.add_conditions_btn = Button(
            page,
            locator='data-testid=create_campaigns_conditions_add_description',
            name='Добавить описание требований и ограничений',
        )
        self.add_geo_targeting_btn = Button(
            page,
            locator='[data-testid="create_campaigns_geography_add_description"]',
            name="Добавить описание геотаргетинга"
        )
        self.add_target_audience_btn = Button(
            page,
            locator='data-testid=create_campaigns_target_audience_add_description',
            name='Добавить описание целевой аудитории',
        )
        self.conditions_description_text_area = Input(
            page,
            locator='data-testid=dialog_conditions_description',
            name='Поле для ввода описания требований и ограничений'
        )
        self.geo_targeting_description_text_area = Input(
            page,
            locator='[data-testid="dialog_geography_description"]',
            name='Поле для ввода описания гео таргетинга'
        )
        self.target_audience_description_text_area = Input(
            page,
            locator='[data-testid="dialog_target_audience_description"]',
            name='Поле для ввода описания целевой аудитории'
        )
        self.conditions_description = Button(
            page,
            locator='data-testid=create_campaigns_conditions_description',
            name='Описание требований и ограничений',
        )
        self.geo_targeting_description = Button(
            page,
            locator='[data-testid="create_campaigns_geography_description"]',
            name="Описание геотаргетинга"
        )
        self.target_audience_description = Button(
            page,
            locator='data-testid=create_campaigns_target_audience_description',
            name='Описание целевой аудитории',
        )
        self.co_brand = DropDownList(
            page,
            locator='data-testid=create_digital_campaigns_co-brand_{co_brand_num}',
            name='Ко-бренд',
        )
        self.toastify = Title(
            page, locator='text="Черновик успешно сохранён"', name='Черновик успешно сохранён'
        )
        self.budget = Input(
            page,
            locator='data-testid=create_digital_campaigns_budget',
            name='Бюджет'
        )
        self.save_description_btn = Button(
            page, locator='[data-testid="dialog_confirm"]',
            name='Сохранить'
        )

    def check_geo_from_excel_import(self, cell_title):
        self.geo_targeting_description.should_have_text(cell_title[3][0][0])

    def input_campaign_name(self, digital_test_data: dict) -> None:
        """Ввести название кампании
            Args:
                digital_test_data: массив тестовых данных
        """
        self.create_camp_page.should_be_visible()
        self.campaign_name.fill(digital_test_data['campaign_name'], validate_value=True)

    def input_campaign_naming(self, digital_test_data: dict) -> None:
        """Ввести нейминг кампании
            Args:
                digital_test_data: массив тестовых данных
        """
        self.naming.fill(digital_test_data['campaign_naming'], validate_value=True)

    def select_test_client(self) -> None:
        """Выбор тестового клиента"""
        self.client.select_item_by_text(
            constants.DIGITAL_CLIENT_NAME + ' ' + constants.DIGITAL_CLIENT_NAMING
        )

    def select_test_brand(self) -> None:
        """Выбор тестового бренда"""
        self.brand.select_item_by_text(
            constants.DIGITAL_BRAND_NAME + ' ' + constants.DIGITAL_BRAND_NAMING
        )

    def select_test_product(self) -> None:
        """Выбор тестового продукта"""
        self.product.select_item_by_text(
            constants.DIGITAL_PRODUCT_NAME + ' ' + constants.DIGITAL_PRODUCT_NAMING
        )

    def select_test_agency(self) -> None:
        """Выбор тестового агенства"""
        self.agency.select_item_by_text(
            constants.DIGITAL_AGENCY_NAME + ' ' + constants.DIGITAL_AGENCY_NAMING
        )

    def select_test_department(self) -> None:
        """Выбор тестового подразделения"""
        self.department.select_item_by_text(
            constants.DIGITAL_DEPARTMENT_NAME + ' ' + constants.DIGITAL_DEPARTMENT_NAMING
        )

    def select_co_brand(self, co_brand_num: str) -> None:
        """Добавление ко-бренда
        Args:
            co_brand_num: номер бренда начиная с 0
        """
        self.co_brand.click(co_brand_num=co_brand_num)
        self.page.get_by_role(
            'option',
            name=f'{constants.DIGITAL_CO_BRAND_NAME} '
                 + f'{constants.DIGITAL_CO_BRAND_NAMING}',
        ).click()

    def input_budget(self) -> None:
        """Метод добавления бюджета"""
        self.budget.fill(f'{MetricsCalculator.BUDGET}')

    def save_draft_click(self) -> None:
        """Сохранение черновика кампании"""
        self.save_campaign.should_be_visible()
        self.save_draft.click()

    def save_campaign_click(self) -> None:
        """Сохранение кампании"""
        self.save_campaign.should_be_visible()
        self.save_campaign.click()

    def check_default_campaign_begin_date(self) -> None:
        """Проверка наличия дефолтного значения даты начала кампании"""
        self.campaign_begin.should_have_value(
            get_default_campaign_begin_date_for_ui()
        )

    def check_default_campaign_end_date(self) -> None:
        """Проверка наличия дефолтного значения даты завершения кампании"""
        self.campaign_end.should_have_value(get_default_campaign_end_date_for_ui())

    def add_conditions_description(self) -> None:
        """Добавить текст описания требований и ограничений"""
        self.add_conditions_btn.hover()
        self.add_conditions_btn.click()
        self.conditions_description_text_area.fill(constants.CONDITIONS_DESCRIPTION_TEXT)
        text = self.page.get_by_test_id('dialog_conditions_description').inner_html()
        assert text == constants.CONDITIONS_DESCRIPTION_TEXT
        self.save_description_btn.click()

    def add_geo_targeting_description(self) -> None:
        """Добавление гео таргетинга в форме создания Рекламной Кампании"""
        self.add_geo_targeting_btn.hover()
        self.add_geo_targeting_btn.click()
        self.geo_targeting_description_text_area.fill(constants.GEO_TARGETING_DESCRIPTION_TEXT)
        text = self.page.get_by_test_id('dialog_geography_description').inner_html()
        assert text == constants.GEO_TARGETING_DESCRIPTION_TEXT
        self.save_description_btn.click()

    def add_target_audience_description(self) -> None:
        """Добавить текст описания целевой аудитории"""
        self.add_target_audience_btn.hover()
        self.add_target_audience_btn.click()
        self.target_audience_description_text_area.fill(constants.TARGET_AUDIENCE_DESCRIPTION_TEXT)
        text = self.page.get_by_test_id('dialog_target_audience_description').inner_html()
        assert text == constants.TARGET_AUDIENCE_DESCRIPTION_TEXT
        self.save_description_btn.click()

    def create_draft_campaign_full(self, digital_test_data: dict) -> None:
        """Создание черновика кампании с полностью заполнеными полями
        Args:
            digital_test_data: словарь названием и неймингом кампании
        """
        self.input_campaign_name(digital_test_data)
        self.input_campaign_naming(digital_test_data)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.select_test_client()
        self.select_test_agency()
        self.select_test_brand()
        self.select_test_product()
        self.select_test_department()
        self.select_co_brand('0')
        self.input_budget()
        self.add_conditions_description()
        self.add_geo_targeting_description()
        self.add_target_audience_description()
        self.save_draft_click()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Черновик успешно создан', '']

    def create_draft_campaign_part(self, digital_test_data: dict) -> None:
        """Создание черновика кампании с частично заполнеными полями
        Args:
            digital_test_data: массив тестовых данных
        """
        self.input_campaign_name(digital_test_data)
        self.input_campaign_naming(digital_test_data)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.select_test_client()
        self.select_test_brand()
        self.select_test_product()
        self.save_draft_click()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Черновик успешно создан', '']

    def create_campaign_full(self, digital_test_data: dict) -> None:
        """Создание кампании с полностью заполнеными полями
        Args:
            digital_test_data: массив тестовых данных
        """
        self.input_campaign_name(digital_test_data)
        self.input_campaign_naming(digital_test_data)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.select_test_client()
        self.select_test_agency()
        self.select_test_department()
        self.select_test_brand()
        self.select_test_product()
        self.select_co_brand('0')
        self.input_budget()
        self.add_conditions_description()
        self.add_geo_targeting_description()
        self.add_target_audience_description()
        self.save_campaign_click()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Кампания успешно создана', '']

    def create_campaign_part(self, digital_test_data: dict) -> None:
        """Создание кампании с частично заполнеными полями
        Args:
            digital_test_data: массив тестовых данных
        """
        self.input_campaign_name(digital_test_data)
        self.input_campaign_naming(digital_test_data)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.select_test_client()
        self.select_test_brand()
        self.select_test_product()
        self.save_campaign_click()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Кампания успешно создана', '']

    def update_data_and_save_draft(
            self, updated_data_for_campaign: dict
    ) -> None:
        """Отредактировать название и  нейминг черновика кампании для повтора"""
        self.campaign_name.fill(updated_data_for_campaign['new_campaign_name'])
        self.input_campaign_naming(updated_data_for_campaign['new_campaign_naming'])
        self.save_draft_click()

    def update_data_and_save_campaign(
            self, updated_data_for_campaign: dict
    ) -> None:
        """Отредактировать название и  нейминг кампании для повтора"""
        self.campaign_name.fill(updated_data_for_campaign['new_campaign_name'])
        self.input_campaign_naming(updated_data_for_campaign['new_campaign_naming'])
        self.save_campaign_click()


class DigitalAboutCampaign(DigitalCreateCampaign):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page: Page = page

    def check_created_draft_campaign_full(
            self, campaign_name: str, campaign_naming: str
    ) -> None:
        """Проверка созданного черновика кампании. Все поля заполнены
        Args:
            campaign_name: название кампании
            campaign_naming: нейминг кампании
        """
        self.client.should_have_text(
            f'{constants.DIGITAL_CLIENT_NAME} {constants.DIGITAL_CLIENT_NAMING}'
        )
        self.agency.should_have_text(
            f'{constants.DIGITAL_AGENCY_NAME} {constants.DIGITAL_AGENCY_NAMING}'
        )
        self.brand.should_have_text(
            f'{constants.DIGITAL_BRAND_NAME} {constants.DIGITAL_BRAND_NAMING}'
        )
        self.product.should_have_text(
            f'{constants.DIGITAL_PRODUCT_NAME} {constants.DIGITAL_PRODUCT_NAMING}'
        )
        self.co_brand.should_have_text(
            f'{constants.DIGITAL_CO_BRAND_NAME} {constants.DIGITAL_CO_BRAND_NAMING}',
            co_brand_num=0,
        )
        self.campaign_name.should_have_value(campaign_name)
        self.naming.should_have_value(campaign_naming)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.conditions_description.should_have_text(constants.CONDITIONS_DESCRIPTION_TEXT)
        self.geo_targeting_description.should_have_text(constants.GEO_TARGETING_DESCRIPTION_TEXT)
        self.target_audience_description.should_have_text(constants.TARGET_AUDIENCE_DESCRIPTION_TEXT)

    def check_created_draft_campaign_part(
            self, campaign_name: str, campaign_naming: str
    ) -> None:
        """Проверка созданного черновика кампании. Заполнены только обязательные поля
        Args:
            campaign_name: название кампании
            campaign_naming: нейминг кампании
        """
        self.client.should_have_text(
            f'{constants.DIGITAL_CLIENT_NAME} {constants.DIGITAL_CLIENT_NAMING}'
        )
        self.brand.should_have_text(
            f'{constants.DIGITAL_BRAND_NAME} {constants.DIGITAL_BRAND_NAMING}'
        )
        self.product.should_have_text(
            f'{constants.DIGITAL_PRODUCT_NAME} {constants.DIGITAL_PRODUCT_NAMING}'
        )
        self.campaign_name.should_have_value(campaign_name)
        self.naming.should_have_value(campaign_naming)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()

    def check_created_campaign_full(self, campaign_name: str, campaign_naming: str) -> None:
        """Проверка созданной кампании. Все поля заполнены
        Args:
            campaign_name: название кампании
            campaign_naming: нейминг кампании
        """
        self.client.should_have_text(
            f'{constants.DIGITAL_CLIENT_NAME} {constants.DIGITAL_CLIENT_NAMING}'
        )
        self.agency.should_have_text(
            f'{constants.DIGITAL_AGENCY_NAME} {constants.DIGITAL_AGENCY_NAMING}'
        )
        self.brand.should_have_text(
            f'{constants.DIGITAL_BRAND_NAME} {constants.DIGITAL_BRAND_NAMING}'
        )
        self.product.should_have_text(
            f'{constants.DIGITAL_PRODUCT_NAME} {constants.DIGITAL_PRODUCT_NAMING}'
        )
        self.co_brand.should_have_text(
            f'{constants.DIGITAL_CO_BRAND_NAME} {constants.DIGITAL_CO_BRAND_NAMING}',
            co_brand_num=0,
        )
        self.department.should_have_text(
            f'{constants.DIGITAL_DEPARTMENT_NAME} {constants.DIGITAL_DEPARTMENT_NAMING}',
        )
        self.campaign_name.should_have_value(campaign_name)
        self.naming.should_have_value(campaign_naming)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.conditions_description.should_have_text(constants.CONDITIONS_DESCRIPTION_TEXT)
        self.geo_targeting_description.should_have_text(constants.GEO_TARGETING_DESCRIPTION_TEXT)
        self.target_audience_description.should_have_text(constants.TARGET_AUDIENCE_DESCRIPTION_TEXT)

    def check_created_campaign_part(self, campaign_name: str, campaign_naming: str) -> None:
        """Проверка созданного черновика кампании. Заполнены только обязательные поля
        Args:
            campaign_name: название кампании
            campaign_naming: нейминг кампании
        """
        self.client.should_have_text(
            f'{constants.DIGITAL_CLIENT_NAME} {constants.DIGITAL_CLIENT_NAMING}'
        )
        self.brand.should_have_text(
            f'{constants.DIGITAL_BRAND_NAME} {constants.DIGITAL_BRAND_NAMING}'
        )
        self.product.should_have_text(
            f'{constants.DIGITAL_PRODUCT_NAME} {constants.DIGITAL_PRODUCT_NAMING}'
        )
        self.campaign_name.should_have_value(campaign_name)
        self.naming.should_have_value(campaign_naming)
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
