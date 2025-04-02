import time
from datetime import date
from urllib.parse import urlparse
from playwright.sync_api import Page
from controller.button import Button
from controller.input import Input
from controller.list_item import ListItem
from controller.table_new import Table
from controller.title import Title
from controller.drop_down_list import DropDownList
from controller.tabbar import Tabbar
from user_office import constants
from helper.default_dates import get_default_campaign_begin_date_for_ui, get_default_campaign_end_date_for_ui
from helper.calendar_helper import get_count_of_days_by_dates
from helper.value_handler import value_handler_decimal, value_handler_decimal_prc
from db_stuff.db_interactions.sources_db_interactions import get_source_name_by_id
from db_stuff.db_interactions.channels_db_interactions import get_channel_name_by_naming
from db_stuff.db_interactions.buy_types_db_interactions import get_buy_type_name_by_id
from db_stuff.db_interactions.ad_formats_db_interactions import get_ad_format_name_by_id
from db_stuff.db_interactions.ad_sizes_db_interactions import get_ad_size_name_by_id
from db_stuff.db_interactions.metrics_db_interactions import get_metric_name_by_code
from db_stuff.db_interactions.sellers_db_interactions import get_seller_name_by_id


class DigitalMediaplan:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

        self.mediaplan_status = Title(
            page=page,
            locator='[data-testid="mediaplan_digital_status"]',
            name="Статус медиаплана",
        )
        self.mediaplan_information = Title(
            page=page,
            locator='[data-testid="mediaplan_digital_information"]',
            name="Информация медиаплана",
        )
        self.add_placement_button = Button(
            page=page,
            locator='[data-testid="mediaplan_digital_add_placement_button_"]',
            name="​ Добавить размещение",
        )
        self.add_placement_from_template_button = Button(
            page=page,
            locator='[data-testid="mp_digital_add_placement_of_directory_"]',
            name="Добавить размещение из справочника",
        )
        self.placement_template_from_dictionary = ListItem(
            page=page,
            locator='[data-testid="dialog_placement_template_{row}"]',
            name='Шаблон размещения из справочника. row - номер шаблона начиная с 0'
        )
        self.dialog_confirm = Button(
            page=page,
            locator='[data-testid="dialog_confirm"]',
            name='Кнопка подтверждения выбора в модальном окне справочника размещений'
        )
        self.placement_context_menu_button = Button(
            page=page,
            locator='[data-testid="mp-view-menu"]',
            name="Контекстное меню размещения",
        )
        self.table_placements = Table(
            page=page, locator='[data-testid="mediaplan_digital_table_with_placements_DIS"]', name="Таблица размещений"
        )
        self.publish_completed = Button(
            page=page,
            locator='[data-testid="instructions_publication_completed"]',
            name="Кнопка Публикация завершена",
        )
        self.back_to_campaign_page = Button(
            page=page,
            locator='[data-testid="mediaplan_digital_back_button"]',
            name="Кнопка возврата на страницу кампании",
        )
        self.add_placement_btn = Button(
            page=page,
            locator='[data-testid="mediaplan_digital_add_placement_button_"]',
            name="​ Добавить размещение",
        )
        self.filled_button = Button(
            page,
            locator="text='Заполнено'",
            name="Заполнено"
        )
        self.in_progress_button = Button(
            page,
            locator="text='В работе'",
            name="В работе"
        )
        self.zero_placements_group = Button(
            page=page,
            locator="[data-testid='mediaplan_digital_placements_group_name_0']",
            name="Первая группа размещений",
        )

        self.one_placements_group = Button(
            page=page,
            locator="[data-testid='mediaplan_digital_placements_group_name_1']",
            name="Вторая группа размещений",
        )
        self.pagination_for_article = Button(
            page=page,
            locator="[data-testid='mediaplan_digital_pagination_with_placements_article_{number}']",
            name="Пагинация",
        )
        self.pagination_for_dis = Button(
            page=page,
            locator="[data-testid='mediaplan_digital_pagination_with_placements_DIS_{number}']",
            name="Пагинация",
        )
        self.btn_next_artice = Title(
            page=page,
            locator="[data-testid='mediaplan_digital_pagination_with_placements_article_next']",
            name="Следующая страница",
        )
        self.btn_next_dis = Title(
            page=page,
            locator="[data-testid='mediaplan_digital_pagination_with_placements_DIS_next']",
            name="Следующая страница",
        )
        self.checked = Button(
            page=page,
            locator="item-checkbox_DIS_0",
            name="Чекбокс"
        )
        self.global_checkbox = Button(
            page=page,
            locator="global-checkbox",
            name="Глобальный чекбокс"
        )
        self.aprove_button = Button(
            page=page,
            locator="[data-testid='mediaplan_digital_approve_placements_button_']",
            name="Утвердить выбранное"
        )
        self.analytics_tab = Tabbar(
            page=page,
            locator="text='Аналитика'",
            name="Вкладка Аналитика"
        )
        self.table = Table(page, locator='//table', name='Таблица медиапланов')

    def check_in_filled_from_import_excel(self, digital):
        self.table.should_have_text_cell_in_row(
            check_text=digital[0][2], number_cell=2, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text=digital[2][0], number_cell=3, number_row=0
        )
        self.table.should_have_text_cell_in_row(
            check_text=constants.IN_PROGRESS_PLACEMENT_STATUS, number_cell=7, number_row=0
        )

    def checkbox_check(self):
        """Установка чек бокса для утверждения размещений и проверка,
        что чек бокс установлен и проверка утверждённого статуса МП
        """
        self.page.get_by_test_id("item-checkbox_DIS_0").check()
        self.page.get_by_test_id("item-checkbox_DIS_0").is_checked()
        self.aprove_button.click()
        self.page.get_by_test_id("global-checkbox").is_disabled()
        self.mediaplan_status.should_have_text(text='Утвержден')

    def open_campaign_page(self) -> None:
        """Перейти на страницу кампании"""
        self.back_to_campaign_page.click()

    def check_new_mediaplan_planning_status_through_mp_page(
            self, campaign_naming: str
    ) -> None:
        """Проверка даты создания, статуса и принадлежности кампании по неймингу"""
        self.mediaplan_status.should_have_text(constants.PLANNING_STATUS)
        self.mediaplan_information.should_have_text(
            f"Кампания {campaign_naming} |"
            f' Создана {date.today().strftime("%d.%m.20%y")}'
        )

    def pagination_in_page_mediaplan_1_level(self):
        for i in range(2, 10):
            """Метод будет убран как только решу проблему проверки is_enabled"""
            if (
                    self.page.locator(
                        "[data-testid='mediaplan_digital_pagination_with_placements_article_next']"
                    ).is_enabled()
                    == True
            ):
                # TODO: Позже переделаю проверки в рамках задачи - удаления пустых МП и РК https://jira.mts.ru/browse/MDP-5934
                assert (
                        self.page.get_by_role(role="row").count() == 11
                ), "Рамещений меньше 10 на странице"
                self.page.locator(
                    "[data-testid='mediaplan_digital_pagination_with_placements_article_next']"
                ).click()
        else:
            False

    def pagination_in_page_mediaplan_2_level(self):
        self.zero_placements_group.click()
        self.one_placements_group.click()
        for i in range(2, 10):
            """Метод будет убран как только решу проблему проверки is_enabled"""
            if (
                    self.page.locator(
                        "[data-testid='mediaplan_digital_pagination_with_placements_DIS_next']"
                    ).is_enabled()
                    == True
            ):
                # TODO: Позже переделаю проверки в рамках задачи - удаления пустых МП и РК https://jira.mts.ru/browse/MDP-5934
                assert self.page.get_by_role(
                    role="row", name="МТС DSP"
                ), "Тест в размещении не отображается"
                self.page.locator(
                    "[data-testid='mediaplan_digital_pagination_with_placements_DIS_next']"
                ).click()
        else:
            False

    def check_new_placement_draft(self, placement_name: str) -> None:
        """Проверка создания нового размещения в статусе В работе
        Args:
            placement_name: имя размещения
        """
        self.table_placements.should_have_text_cell_in_row(
            check_text=placement_name, number_cell=1, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_SOURCE_MY_TARGET_NAME, number_cell=2, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.IN_PROGRESS_PLACEMENT_STATUS, number_cell=7, number_row=0
        )

    def check_new_placement_filled_status(self, placement_name: str) -> None:
        """Проверка создания нового размещения в статусе Заполнено
        Args:
            placement_name: имя размещения
        """
        self.table_placements.hover()
        self.table_placements.should_be_visible()
        self.table_placements.should_have_text_cell_in_row(
            check_text=placement_name, number_cell=1, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_SOURCE_MTS_DSP_NAME, number_cell=2, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.FILLED_PLACEMENT_STATUS, number_cell=8, number_row=0
        )

    def check_retried_placement_completed_status_in_placements_list(
            self, placement_name: str, budget_value: str
    ) -> None:
        """Проверка повтора размещения в статусе Заполнено
        Args:
            placement_name: имя размещения
            budget_value: значение метрики Бюджет
        """
        self.table_placements.hover()
        self.table_placements.should_be_visible()
        self.table_placements.should_have_text_cell_in_row(
            check_text=placement_name, number_cell=1, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_SOURCE_MY_TARGET_NAME, number_cell=1, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_FORMAT_HTML5_NAME, number_cell=2, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_BUY_TYPE_CPM_NAME, number_cell=3, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=budget_value + " ₽", number_cell=4, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.FILLED_PLACEMENT_STATUS, number_cell=6, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.IN_PROGRESS_PLACEMENT_STATUS, number_cell=7, number_row=0
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=f"2_{constants.DIGITAL_SOURCE_MY_TARGET_NAME}_{constants.DIGITAL_CHANNEL_DISPLAY_NAME}_"
                       f"{constants.DIGITAL_BUY_TYPE_CPM_NAME}_{constants.DIGITAL_FORMAT_HTML5_NAME.replace(' ', '')}",
            number_cell=0,
            number_row=1,
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_SOURCE_MY_TARGET_NAME, number_cell=1, number_row=1
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_FORMAT_HTML5_NAME, number_cell=2, number_row=1
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.DIGITAL_BUY_TYPE_CPM_NAME, number_cell=3, number_row=1
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=budget_value + " ₽", number_cell=4, number_row=1
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.FILLED_PLACEMENT_STATUS, number_cell=6, number_row=1
        )
        self.table_placements.should_have_text_cell_in_row(
            check_text=constants.PUBLISHED_PLACEMENT_STATUS, number_cell=7, number_row=1
        )

    def open_connection_settings_through_placements_list(self) -> None:
        """Открыть настройки подключений нажатием на название размещения"""
        self.table_placements.click_cell_in_row_by_num(number_row=0, number_cell=0)

    def open_connection_settings_through_context_menu(self) -> None:
        """Открыть настройки подключений из контекстного меню"""
        self.table_placements.click_cell_in_row_by_num(number_row=0, number_cell=10)
        self.page.get_by_role("button", name="Настройки подключений").click()

    def open_placement_by_name(self, placement_name: str) -> None:
        """Открыть настройки подключений из контекстного меню"""
        self.page.get_by_role("link", name=placement_name).click()

    def open_instructions_publication_from_context_menu(self) -> None:
        """Открыть инструкцию по публикации из контекстного меню"""
        self.table_placements.click_cell_in_row_by_num(number_row=0, number_cell=10)
        self.page.get_by_role("button", name="Инструкция по публикации").click()

    def retry_placement(self) -> None:
        """Открыть повтор размещения из контекстного меню"""
        self.table_placements.click_cell_in_row_by_num(number_row=0, number_cell=9)
        self.page.get_by_role("button", name="Повторить").click()

    def approve_placement(self) -> None:
        """Утвердить размещение"""
        self.table_placements.click_cell_in_row_by_num(number_row=0, number_cell=10)
        self.page.get_by_role("button", name="Утвердить").click()

    def publish_placement(self) -> None:
        """Опубликовать размещение в самой первой строке списка"""
        self.table_placements.click_cell_in_row(number_row=0, text_cell="Публикация")
        self.publish_completed.click()

    def add_placement_to_templates(self) -> None:
        """Добавить размещение в справочник"""
        self.table_placements.click_cell_in_row_by_num(
            number_row=0, number_cell=10
        )
        self.page.get_by_role('button', name='Добавить в справочник').click()

    def add_placement_from_templates_without_conversions(self, digital_test_data: dict) -> None:
        """Метод добавления размещения из справочника без конверсий
            Args:
                digital_test_data: массив тестовых данных
                    digital_test_data['source_id_mts_dsp']: id площадки
                    digital_test_data['channel_naming']: Нейминг канала
                    digital_test_data['buy_type_id']: id типа закупки
                    digital_test_data['ad_format_id']: id формата
                    digital_test_data['ad_size_id']: id размера
            Данные нужны для наименований тестовых данных из БД для проверки корректности названия шаблона размещения
        """
        source_name = get_source_name_by_id(digital_test_data['source_id_mts_dsp'])
        channel_name = get_channel_name_by_naming(digital_test_data['channel_naming'])
        buy_type_name = get_buy_type_name_by_id(digital_test_data['buy_type_id'])
        ad_format_name = get_ad_format_name_by_id(digital_test_data['ad_format_id'])
        ad_size_name = get_ad_size_name_by_id(digital_test_data['ad_size_id'])
        template_name = source_name + ' | ' + channel_name + ' | ' + buy_type_name + ' | ' + ad_format_name + ' | ' \
                        + ad_size_name + ' | Без конверсий'
        self.add_placement_from_template_button.click()
        self.placement_template_from_dictionary.should_have_text(template_name, row=0)
        self.placement_template_from_dictionary.click(row=0)
        self.dialog_confirm.click()

    def add_placement(self) -> None:
        """Переход к созданию размещения"""
        self.add_placement_btn.click()

    def open_placement_context_menu(self) -> None:
        """Открыть контекстное меню размещения"""
        self.placement_context_menu_button.click()

    def go_back_to_campaign_page(self) -> None:
        """Переход к странице кампании"""
        self.back_to_campaign_page.click()

    def click_filled_button_for_placement(self):
        """Изменить статус Размещения на 'Заполнено'"""
        self.filled_button.should_be_visible()
        self.filled_button.click()

    def click_in_progress_button_for_placement(self):
        """Изменить статус Размещения на 'Заполнено'"""
        self.in_progress_button.should_be_visible()
        self.in_progress_button.click()

    def open_analytics_tab(self):
        """Открыть вкладку Аналитика"""
        self.analytics_tab.should_be_visible()
        self.analytics_tab.click()


class DigitalCreateMediaplan:
    def __init__(self, page: Page) -> None:
        self.table_draft = Table(page, locator="Черновик", name="Черновик")
        self.page: Page = page
        self.create_btn = Button(
            page=page,
            locator="text='Создать медиаплан'",
            name="Создать Медиаплан",
        )
        self.create_draft_btn = Button(
            page=page,
            locator="text='Сохранить черновик'",
            name="Сохранить черновик",
        )
        self.landing_link = Input(
            page=page,
            locator="[data-testid='createmediaplan_landings_']",
            name="Вставьте ссылки на лендинги",
        )
        self.save_constrains = Button(
            page=page, locator="text='Сохранить'", name="Сохранить"
        )

        self.add_targeting = Button(
            page=page,
            locator="[data-testid='createmediaplan_button_add_targetings_']",
            name="Таргетинг",
        )
        self.landing_link2 = Input(
            page=page,
            locator="[data-testid='createmediaplan_landings_1']",
            name="Вставьте ссылки на лендинги",
        )

    def create_mediaplan(self) -> None:
        """Кнопка сохранения и создания медиаплана"""
        self.create_btn.hover()
        self.create_btn.should_be_visible()
        self.create_btn.click()

    def create_draft_mediaplan(self) -> None:
        """Кнопка сохранения черновика медиаплана"""
        self.create_draft_btn.hover()
        self.create_draft_btn.should_be_visible()
        self.create_draft_btn.click()

    def input_landing_2_links(self) -> None:
        """Ввести лендинг"""
        self.landing_link.click()
        self.landing_link.fill(f"{constants.DIGITAL_LANDING_LINK_ALT}\n" f"{constants.DIGITAL_LANDING_LINK}")

    def input_landing(self) -> None:
        """Ввести лендинг"""
        self.landing_link.click()
        self.landing_link.fill(constants.DIGITAL_LANDING_LINK)

    def create_mplan(self) -> None:
        """Создание медиаплана
        Args:
        """
        self.input_landing()
        self.create_mediaplan()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Медиаплан создан', ''], 'Тост сообщение отличается'

    def create_draft_mp(self):
        """
        Проверка созданного черновика медиаплана
        """
        self.input_landing()
        self.create_draft_mediaplan()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Черновик сохранён', ''], 'Тост сообщение отличается'

    def create_draft_mplan(self) -> None:
        """Создание медиаплана
        """
        self.input_landing()
        self.create_draft_mediaplan()
        text = self.page.get_by_role(role='alert').all_inner_texts()
        assert text == ['Черновик сохранён', ''], 'Тост сообщение отличается'


class DigitalExportMP:
    """
    Модель для экспорта xlsx-файла медиаплана
    """

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.export_button = Button(
            page=page,
            locator='[data-testid="mediaplan_digital_export_xls_button"]',
            name="Экспорт в XLS",
        )

    def export(self) -> str | None:
        """Находит и нажимает кнопку 'Экспорт в xls'"""
        self.export_button.should_be_visible()
        with self.page.expect_download() as download_info:
            # Perform the action that initiates download
            self.export_button.click()
        return download_info.value.save_as(constants.SIMPLE_MPLAN_XLS_EXPORT)

    def get_id_from_url(self, position=-1) -> str:
        """Получает id (рекламной кампании, медиаплана или размещения
        можно задать индекс, по которому функция получит не
        последний кусок урла, а предпоследний, или любой другой"""
        self.page.reload()
        some_url_with_id = self.page.url
        required_id = urlparse(some_url_with_id).path.split("/")[position]
        return required_id


class DigitalMplanAnalytics:

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.metric_drop_down_list = DropDownList(
            page=page,
            locator='[data-testid="mediaplan_analytics_metrics_select"]',
            name="Выпадающий список метрик"
        )
        self.mediaplan_analytics_placements_budget_per_month_table_row = Title(
            page=page,
            locator='[data-testid="mediaplan_analytics_budget_per_month_table_row-{row}"]',
            name='Распределение бюджета по месяцам. row: номер строки таблицы'
        )
        self.mediaplan_analytics_budget_per_seller_table_row = Title(
            page=page,
            locator='[data-testid="mediaplan_analytics_budget_per_seller_table_row-{row}"]',
            name='Распределение бюджета по продавцам. row: номер строки таблицы'
        )
        self.mediaplan_analytics_placements_budget_table_row = Title(
            page=page,
            locator='[data-testid="mediaplan_analytics_placements_budget_table_row-{row}"]',
            name='Бюджет по статусам размещений. row: номер строки таблицы'
        )
        self.mediaplan_analytics_placements_budget_chart_legend = Title(
            page=page,
            locator='[data-testid="mediaplan_analytics_placements_budget_chart_legend"]',
            name='Легенда диаграммного виджета'
        )

    def check_mediaplan_analytics_tables_planning_status(self, campaign_budget: str) -> True | False:
        """Проверка таблиц во вкладке Аналитика страницы медиаплана. Статус Планирование
            Args:
                campaign_budget: бюджет кампании
        """
        formatted_value = value_handler_decimal(float(campaign_budget))
        self.mediaplan_analytics_placements_budget_per_month_table_row.should_have_text(
            'Итого0,000%', row=0
        )
        self.mediaplan_analytics_budget_per_seller_table_row.should_have_text(
            'Итого0,000%', row=0
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            'В работе0,000%', row=0
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            'Заполнено0,000%', row=1
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            'Остаток' + formatted_value + '100%', row=2
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            'Бюджет Кампании' + formatted_value + '100%', row=3
        )

    def check_mediaplan_analytics_tables_approved_status(
            self, campaign_budget: str, placement_budget: str, seller_name: str
    ) -> True | False:
        """Проверка таблиц во вкладке Аналитика страницы медиаплана. Статус Утвержден
            Args:
                campaign_budget: бюджет кампании
                placement_budget: бюджет размещения
                seller_name: наименование продавца
        """
        # Получаем кол-во дней по месяцам
        days_in_period = get_count_of_days_by_dates(
            get_default_campaign_begin_date_for_ui(), get_default_campaign_end_date_for_ui()
        )
        days_keys = list(days_in_period.keys())
        days_values = list(days_in_period.values())
        # Вычисляем остаток бюджета
        budget_remaining = float(campaign_budget) - float(placement_budget)
        # Вычисляем общее количество дней и процентное соотношение бюджета для каждого месяца
        total_days = sum(days_values)
        first_month_prc = round((days_values[0] / total_days) * 100, 2)
        second_month_prc = round((days_values[1] / total_days) * 100, 2)
        # Вычисляем процентное соотношение бюджета размещения и остатка от общего бюджета кампании
        placement_budget_prc = round(float(placement_budget) / (float(campaign_budget) / 100), 2)
        budget_remaining_prc = round(float(budget_remaining) / (float(campaign_budget) / 100), 2)
        # Вычисляем бюджет размещения для каждого месяца
        budget_ratio = int(placement_budget) / total_days
        first_month_placement_budget = budget_ratio * days_values[0]
        second_month_placement_budget = budget_ratio * days_values[1]
        # Форматируем числа для вывода
        formatted_first_month_placement_budget = value_handler_decimal(float(first_month_placement_budget))
        formatted_second_month_placement_budget = value_handler_decimal(float(second_month_placement_budget))
        formatted_total_placement_budget = value_handler_decimal(int(placement_budget))
        formatted_campaign_budget = value_handler_decimal(float(campaign_budget))
        formatted_budget_remaining = value_handler_decimal(budget_remaining)
        formatted_placement_budget_prc = value_handler_decimal_prc(placement_budget_prc)
        formatted_first_month_prc = value_handler_decimal_prc(first_month_prc)
        formatted_second_month_prc = value_handler_decimal_prc(second_month_prc)
        formatted_budget_remaining_prc = value_handler_decimal_prc(budget_remaining_prc)
        self.mediaplan_analytics_placements_budget_per_month_table_row.should_have_text(
            f'{days_keys[0] + formatted_first_month_placement_budget + formatted_first_month_prc}%', row=0
        )
        self.mediaplan_analytics_placements_budget_per_month_table_row.should_have_text(
            f'{days_keys[1] + formatted_second_month_placement_budget + formatted_second_month_prc}%', row=1
        )
        self.mediaplan_analytics_placements_budget_per_month_table_row.should_have_text(
            f'Итого{formatted_total_placement_budget}100%', row=2
        )
        self.mediaplan_analytics_budget_per_seller_table_row.should_have_text(
            f'{seller_name + formatted_total_placement_budget}100%', row=0
        )
        self.mediaplan_analytics_budget_per_seller_table_row.should_have_text(
            f'Итого{formatted_total_placement_budget}100%', row=1
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            'В работе0,000%', row=0
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            f'Заполнено{formatted_total_placement_budget + formatted_placement_budget_prc}%', row=1
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            f'Остаток{formatted_budget_remaining + formatted_budget_remaining_prc}%', row=2
        )
        self.mediaplan_analytics_placements_budget_table_row.should_have_text(
            f'Бюджет Кампании{formatted_campaign_budget}100%', row=3
        )

    def check_analytics_page_planning_status(self, digital_test_data: dict, campaign_budget: str) -> True | False:
        """Проверка раздела Аналитика на странице медиаплана. Статус Планирование
           Проверка производится с переключением на каждую
           из 3 метрик: Просмотры, Клики, Показы
            Args:
                digital_test_data: массив тестовых данных, из которого берутся коды метрик, для поиска их названий
                campaign_budget: бюджет кампании
        """
        imps_name = get_metric_name_by_code(digital_test_data['metric_code_imps'])
        clicks_name = get_metric_name_by_code(digital_test_data['metric_code_clicks'])
        views_name = get_metric_name_by_code(digital_test_data['views_metric_code'])
        self.metric_drop_down_list.should_have_item(imps_name)
        self.metric_drop_down_list.should_have_item(clicks_name)
        self.metric_drop_down_list.should_have_item(views_name)
        self.metric_drop_down_list.should_have_text(imps_name)
        self.check_mediaplan_analytics_tables_planning_status(campaign_budget)
        self.metric_drop_down_list.select_item_by_text(clicks_name)
        self.check_mediaplan_analytics_tables_planning_status(campaign_budget)
        self.metric_drop_down_list.select_item_by_text(views_name)
        self.check_mediaplan_analytics_tables_planning_status(campaign_budget)
        self.mediaplan_analytics_placements_budget_chart_legend.should_be_visible()

    def check_analytics_page_approved_status(
            self, digital_test_data: dict, campaign_budget: str, placement_budget: str
    ) -> True | False:
        """Проверка раздела Аналитика на странице медиаплана. Статус Утвержден
            Проверка производится с переключением на каждую
            из 3 метрик: Просмотры, Клики, Показы
            Args:
                digital_test_data: массив тестовых данных, из которого берутся коды метрик, для поиска их названий
                campaign_budget: бюджет кампании
                placement_budget: бюджет размещения
        """
        imps_name = get_metric_name_by_code(digital_test_data['metric_code_imps'])
        clicks_name = get_metric_name_by_code(digital_test_data['metric_code_clicks'])
        views_name = get_metric_name_by_code(digital_test_data['views_metric_code'])
        seller_name = get_seller_name_by_id(digital_test_data['seller_id_mts'])
        self.metric_drop_down_list.should_have_item(imps_name)
        self.metric_drop_down_list.should_have_item(clicks_name)
        self.metric_drop_down_list.should_have_item(views_name)
        self.metric_drop_down_list.should_have_text(imps_name)
        self.check_mediaplan_analytics_tables_approved_status(campaign_budget, placement_budget, seller_name)
        self.metric_drop_down_list.select_item_by_text(clicks_name)
        self.check_mediaplan_analytics_tables_approved_status(campaign_budget, placement_budget, seller_name)
        self.metric_drop_down_list.select_item_by_text(views_name)
        self.check_mediaplan_analytics_tables_approved_status(campaign_budget, placement_budget, seller_name)
        self.mediaplan_analytics_placements_budget_chart_legend.should_be_visible()

