from playwright.sync_api import Page, expect
from controller.title import Title
from controller.tabbar import Tabbar
from controller.table_new import Table
from controller.button import Button
from controller.input import Input
from controller.drop_down_list import DropDownList
from modals.dialog_modal import DialogModal
from db_stuff.db_interactions.brands_db_interactions import get_brands_data_by_organization_id
from db_stuff.db_interactions.clients_db_interactions import get_clients_data_by_organization_id
from db_stuff.db_interactions.products_db_interactions import get_products_data_by_organization_id
from db_stuff.db_interactions.organization_links_db_interactions import get_organization_links_data_by_organization_id
from db_stuff.db_interactions.organizations_db_interactions import get_organization_by_email
from user_office import constants


class Dictionaries:
    def __init__(self, page: Page):
        self.page = page
        self.naming_tab = Tabbar(
            page,
            locator='text="Нейминг"',
            name="Нейминг"
        )
        self.templates_tab = Tabbar(
            page,
            locator='text="Сценарии"',
            name="Сценарии"
        )
        self.customization = Tabbar(
            page,
            locator='text="Кастомизация"',
            name="Кастомизация"
        )
        self.relations = Tabbar(
            page,
            locator='text="Связи"',
            name="Связи"
        )
        self.digital_dictionaries_tab = Tabbar(
            page,
            locator='text="Digital кампании"',
            name="Digital кампании"
        )
        self.brands_dictionary = Title(
            page,
            locator="//span[.='Бренды']",
            name='Бренды'
        )
        self.clients_dictionary = Title(
            page,
            locator="//span[.='Клиенты']",
            name='Клиенты'
        )
        self.products_dictionary = Title(
            page,
            locator="//span[.='Продукты']",
            name='Продукты'
        )
        self.tv_campaign_dictionary = Title(
            page,
            locator='text="ТВ кампании"',
            name="ТВ кампании"
        )
        self.table = Table(
            page=page, locator="//table", name="Таблица элементов справочников"
        )
        self.next_page_pagination = Button(
            page,
            locator="[data-testid='undefined_next']",
            name='Следующая страница'
        )
        self.prev_page_pagination = Button(
            page,
            locator="[data-testid='undefined_prev']",
            name='Предыдущая страница'
        )
        self.placement_templates_list_btn = Button(
            page,
            locator="//span[.='Сценарии размещений']",
            name='Сценарии размещений'
        )
        self.create_placement_template_btn = Button(
            page,
            locator="[data-testid='placements_templates_list_create_button']",
            name='Кнопка перехода к созданию сценария размещения'
        )

    def check_dictionary(self, data: list) -> None:
        """Метод проверяет каждую запись каждой страницы справочника.
            Args:
                data: массив данных справочника
        """
        current_row = 0
        for i, page in enumerate(data, start=1):
            for row in page:
                for cell_number, cell_data in enumerate(row):
                    self.table.should_have_text_cell_in_row(check_text=cell_data, number_cell=cell_number,
                                                            number_row=current_row)
                current_row += 1
                if current_row == 10:
                    current_row = 0
                    if i < len(data):
                        self.next_page_pagination.click()

    def check_digital_dict(self) -> True | False:
        """Проверка справочников Digital"""
        organization_id = get_organization_by_email(constants.EMAIL_ORGANIZATION).id
        brands_data = get_brands_data_by_organization_id(organization_id)
        clients_data = get_clients_data_by_organization_id(organization_id)
        products_data = get_products_data_by_organization_id(organization_id)
        organization_links_data = get_organization_links_data_by_organization_id(organization_id)
        self.digital_dictionaries_tab.should_be_visible()
        self.brands_dictionary.click()
        self.check_dictionary(brands_data)
        self.digital_dictionaries_tab.click()
        self.clients_dictionary.click()
        self.check_dictionary(clients_data)
        self.digital_dictionaries_tab.click()
        self.products_dictionary.click()
        self.check_dictionary(products_data)
        self.relations.click()
        self.check_dictionary(organization_links_data)

    def open_placement_templates_list(self):
        """Открыть список сценариев размещения"""
        self.templates_tab.click()
        self.placement_templates_list_btn.click()

    def open_create_placement_template_page(self):
        """Перейти к созданию сценария размещения"""
        self.create_placement_template_btn.click()

    def check_not_saved_placement_template_in_placement_templates_list(self, digital_test_data: dict):
        """Проверка несохраненного сценария размещения в списке сценариев
            Args:
                digital_test_data: массив тестовых данных
        """
        self.table.should_be_visible()
        expect(self.table.cell_with_text_in_row_by_contains_text(
            text_row=digital_test_data['client_name'], text_cell=f"{digital_test_data['site_mts_dsp_name']} | "
            f"{digital_test_data['channel_olv_name']} | {digital_test_data['buy_type_cpm_name']} | "
            f"{digital_test_data['ad_format_instream_bumper_ads_name']} | {digital_test_data['ad_size_1000x10_name']}"
            " | Без конверсий"
            )
        ).not_to_be_visible()

    def check_saved_placement_template_in_placement_templates_list(self, digital_test_data: dict):
        """Проверка сохраненного сценария размещения в списке сценариев
            Args:
                digital_test_data: массив тестовых данных
        """
        self.table.should_be_visible()
        expect(self.table.cell_with_text_in_row_by_contains_text(
            text_row=digital_test_data['client_name'], text_cell=f"{digital_test_data['site_mts_dsp_name']} | "
            f"{digital_test_data['channel_olv_name']} | {digital_test_data['buy_type_cpm_name']} | "
            f"{digital_test_data['ad_format_instream_bumper_ads_name']} | {digital_test_data['ad_size_1000x10_name']}"
            " | Без конверсий"
            )
        ).to_be_visible()

    def check_saved_placement_template_in_placement_templates_list_base_fields(self, digital_test_data: dict):
        """Проверка сохраненного сценария размещения в списке сценариев. Базовые поля
            Args:
                digital_test_data: массив тестовых данных
        """
        self.table.hover()
        self.table.should_be_visible()
        expect(self.table.cell_with_text_in_row_by_contains_text(
            text_row=digital_test_data['client_name'], text_cell=f"{digital_test_data['site_mts_dsp_name']} | "
            f"{digital_test_data['channel_olv_name']} | {digital_test_data['buy_type_cpm_name']} | Без конверсий"
            )
        ).to_be_visible()

    def check_saved_placement_template_in_placement_templates_list_after_update(self, digital_test_data: dict):
        """Проверка сохраненного сценария размещения в списке сценариев после редактирования
            Args:
                digital_test_data: массив тестовых данных
        """
        self.table.hover()
        self.table.should_be_visible()
        expect(self.table.cell_with_text_in_row_by_contains_text(
            text_row=digital_test_data['client_name'], text_cell=f"{digital_test_data['site_mts_dsp_name']} | "
            f"{digital_test_data['channel_display_name']} | {digital_test_data['buy_type_vcpm_name']} | "
            f"{digital_test_data['ad_format_adaptive_html_name']} | {digital_test_data['ad_size_1000x250_name']}"
            " | Без конверсий"
            )
        ).to_be_visible()

    def open_placement_template_through_context_menu(self):
        """Открыть сценарий размещения"""
        self.table.click_cell_in_row_by_num(
            number_row=0, number_cell=4
        )
        self.page.get_by_role("button", name="Редактировать").click()
        # TODO: доработать взаимодействие с контекстным меню https://jira.mts.ru/browse/MDP-6403


class PlacementTemplate:
    def __init__(self, page: Page):
        self.confirmation_dialog = DialogModal(page)
        self.page = page
        self.placement_template_client = DropDownList(
            page,
            locator="[data-testid='placement_template_client']",
            name='Клиент сценария размещения'
        )
        self.placement_template_site = DropDownList(
            page,
            locator="[data-testid='placement_template_siteID']",
            name='Площадка сценария размещения'
        )
        self.placement_template_seller = DropDownList(
            page,
            locator="[data-testid='placement_template_sellerID']",
            name='Продавец сценария размещения'
        )
        self.placement_template_placement_type = DropDownList(
            page,
            locator="[data-testid='placement_template_placement_type']",
            name='Тип размещения сценария размещения'
        )
        self.placement_template_channel = DropDownList(
            page,
            locator="[data-testid='placement_template_channelCode']",
            name='Канал сценария размещения'
        )
        self.placement_template_buy_type = DropDownList(
            page,
            locator="[data-testid='placement_template_buyTypeID']",
            name='Тип закупки сценария размещения'
        )
        self.placement_template_ad_format = DropDownList(
            page,
            locator="[data-testid='placement_template_adFormatID']",
            name='Формат сценария размещения'
        )
        self.placement_template_ad_size = DropDownList(
            page,
            locator="[data-testid='placement_template_ad_sizes']",
            name='Размер сценария размещения'
        )
        self.placement_template_add_metrics_btn = Button(
            page,
            locator="[data-testid='placement_template_add_metrics_button_BENCHMARKS']",
            name='Кнопка добавления метрики'
        )
        self.placement_template_benchmark_metric_name = DropDownList(
            page,
            locator="[data-testid='placement_template_name_metric__benchmarks_{metric_num}']",
            name='Название метрики бенчмарк. metric_num - номер метрики начиная с 0'
        )
        self.placement_template_benchmark_metric_value = Input(
            page,
            locator="[data-testid='placement_template_value_metric__benchmarks_{metric_num}']",
            name='Значение метрики бенчмарк. metric_num - номер метрики начиная с 0'
        )
        self.placement_template_price_metric_name = DropDownList(
            page,
            locator="[data-testid='placement_template_name_metric__price_{metric_num}']",
            name='Значение ценовой метрики. metric_num - номер метрики начиная с 0'
        )
        self.placement_template_price_metric_value = Input(
            page,
            locator="[data-testid='placement_template_value_metric__price_{metric_num}']",
            name='Значение ценовой метрики. metric_num - номер метрики начиная с 0'
        )
        self.placement_template_delete_metric = Input(
            page,
            locator="[data-testid='placement_template_delete_metric_button__price_{metric_num}']",
            name='Удаление метрики. metric_num - номер метрики начиная с 0'
        )
        self.placement_template_back_btn = Button(
            page,
            locator="[data-testid='placement_template_back_button']",
            name='Сохранить изменения'
        )
        self.save_placement_template_btn = Button(
            page,
            locator="[data-testid='placement_template_submit_button']",
            name='Сохранить изменения'
        )

    def select_client(self, client_name: str, client_naming: str) -> None:
        """Добавить клиента для сценария размещения
            Args:
                client_name: название клиента
                client_naming: нейминг клиента
        """
        self.placement_template_client.should_be_visible()
        self.placement_template_client.select_item_by_text(
            client_name + ' ' + client_naming
        )

    def select_site(self, site_name: str) -> None:
        """Добавить площадку для сценария размещения
            Args:
                site_name: название площадки
        """
        self.placement_template_site.should_be_visible()
        self.placement_template_site.select_item_by_text(site_name)

    def select_placement_type(self, placement_type_name: str) -> None:
        """Добавить тип размещения для сценария размещения
            Args:
                placement_type_name: название типа размещения
        """
        self.placement_template_buy_type.should_be_visible()
        self.placement_template_placement_type.select_item_by_text(placement_type_name)

    def select_buy_type(self, buy_type_name: str) -> None:
        """Добавить тип закупки для сценария размещения
            Args:
                buy_type_name: название типа закупки
        """
        self.placement_template_buy_type.should_be_visible()
        self.placement_template_buy_type.select_item_by_text(buy_type_name)

    def select_channel(self, channel_name: str) -> None:
        """Добавить канал для сценария размещения
            Args:
                channel_name: название канала
        """
        self.placement_template_channel.should_be_visible()
        self.placement_template_channel.select_item_by_text(channel_name)

    def select_ad_format(self, ad_format_name: str) -> None:
        """Добавить формат для сценария размещения
            Args:
                ad_format_name: название формата
        """
        self.placement_template_ad_format.should_be_visible()
        self.placement_template_ad_format.select_item_by_text(ad_format_name)

    def select_ad_size(self, ad_size_name: str) -> None:
        """Добавить размер для сценария размещения
            Args:
                ad_size_name: название размера
        """
        self.placement_template_ad_size.should_be_visible()
        self.placement_template_ad_size.select_item_by_text(ad_size_name)

    def add_metric(self, metric_value: str, metric_num: str, metric_name: str) -> None:
        """Добавить метрику для сценария размещения
            Args:
                metric_name: название метрики
                metric_value: значение метрики
                metric_num: номер метрики начиная с 0
        """
        self.placement_template_add_metrics_btn.click()
        self.placement_template_benchmark_metric_name.fill(
            metric_name, metric_num=metric_num
        )
        self.page.keyboard.press(key='Enter')
        self.placement_template_benchmark_metric_value.click(metric_num=metric_num)
        self.placement_template_benchmark_metric_value.fill(
            metric_num=metric_num, value=metric_value
        )

    def delete_metric(self, metric_num: str) -> None:
        """Удалить метрику
            Args:
                metric_num: номер метрики начиная с 0
        """
        self.placement_template_delete_metric.click(metric_num=metric_num)

    def input_price_metric_value(self, metric_num: str, metric_value: str) -> None:
        """Ввести значение ценовой метрики"""
        self.placement_template_price_metric_value.fill(metric_num=metric_num, value=metric_value)

    def fill_placement_template(self, digital_test_data: dict, metric_value: str) -> None:
        """Заполнение сценария размещения
            Args:
                metric_value: значение метрики
                digital_test_data: массив тестовых данных
        """
        self.select_client(digital_test_data['client_name'], digital_test_data['client_naming'])
        self.select_site(digital_test_data['site_mts_dsp_name'])
        self.select_placement_type(digital_test_data['placement_type_din_name'])
        self.select_buy_type(digital_test_data['buy_type_cpm_name'])
        self.select_channel(digital_test_data['channel_olv_name'])
        self.select_ad_format(digital_test_data['ad_format_instream_bumper_ads_name'])
        self.select_ad_size(digital_test_data['ad_size_1000x10_name'])
        self.delete_metric('0')
        self.add_metric(metric_value, '0', digital_test_data['ctr_metric_name'])

    def fill_placement_template_base_fields(self, digital_test_data: dict) -> None:
        """Заполнение сценария размещения. Обязательные поля
            Args:
                digital_test_data: массив тестовых данных
        """
        self.select_client(digital_test_data['client_name'], digital_test_data['client_naming'])
        self.select_site(digital_test_data['site_mts_dsp_name'])
        self.select_placement_type(digital_test_data['placement_type_din_name'])
        self.select_buy_type(digital_test_data['buy_type_cpm_name'])
        self.select_channel(digital_test_data['channel_olv_name'])
        self.delete_metric('0')

    def fill_placement_template_additional_fields(self, digital_test_data: dict, metric_value: str) -> None:
        """Заполнение дополнительных полей сценария размещения
            Args:
                digital_test_data: массив тестовых данных
                metric_value: значение метрики
        """
        self.select_ad_format(digital_test_data['ad_format_instream_bumper_ads_name'])
        self.select_ad_size(digital_test_data['ad_size_1000x10_name'])
        self.add_metric(metric_value, '0', digital_test_data['ctr_metric_name'])

    def update_placement_template_fields(self, digital_test_data: dict) -> None:
        """Редактирование сценария размещения
            Args:
                digital_test_data: массив тестовых данных
        """
        self.select_buy_type(digital_test_data['buy_type_vcpm_name'])
        self.select_channel(digital_test_data['channel_display_name'])
        self.select_ad_format(digital_test_data['ad_format_adaptive_html_name'])
        self.select_ad_size(digital_test_data['ad_size_1000x250_name'])

    def check_saved_placement_template(self, metric_value: str, digital_test_data: dict):
        """Проверка сохраненного сценария размещения
            Args:
                metric_value: значение метрики
                digital_test_data: массив тестовых данных
        """
        self.placement_template_client.should_have_text(
            digital_test_data['client_name'] + ' ' + digital_test_data['client_naming']
        )
        self.placement_template_site.should_have_text(
            digital_test_data['site_mts_dsp_name']
        )
        self.placement_template_placement_type.should_have_text(
            digital_test_data['placement_type_din_name']
        )
        self.placement_template_buy_type.should_have_text(
            digital_test_data['buy_type_cpm_name']
        )
        self.placement_template_channel.should_have_text(
            digital_test_data['channel_olv_name']
        )
        self.placement_template_ad_format.should_have_text(
            digital_test_data['ad_format_instream_bumper_ads_name']
        )
        self.placement_template_ad_size.should_have_text(
            digital_test_data['ad_size_1000x10_name']
        )
        self.placement_template_benchmark_metric_name.should_have_text(
            digital_test_data['ctr_metric_name'], metric_num='0'
        )
        self.placement_template_benchmark_metric_value.should_have_value(
            metric_value, metric_num='0'
        )

    def check_saved_placement_template_base_fields(self, digital_test_data: dict):
        """Проверка сохраненного сценария размещения
            Args:
                metric_value: значение метрики
                digital_test_data: массив тестовых данных
        """
        self.placement_template_client.should_have_text(
            digital_test_data['client_name'] + ' ' + digital_test_data['client_naming']
        )
        self.placement_template_site.should_have_text(
            digital_test_data['site_mts_dsp_name']
        )
        self.placement_template_placement_type.should_have_text(
            digital_test_data['placement_type_din_name']
        )
        self.placement_template_buy_type.should_have_text(
            digital_test_data['buy_type_cpm_name']
        )
        self.placement_template_channel.should_have_text(
            digital_test_data['channel_olv_name']
        )

    def check_saved_placement_template_all_fields_after_update(
            self, digital_test_data: dict, metric_value: str
    ) -> None:
        """Проверка сохраненного сценария размещения
            Args:
                metric_value: значение метрики
                digital_test_data: массив тестовых данных
        """
        self.placement_template_client.should_have_text(
            digital_test_data['client_name'] + ' ' + digital_test_data['client_naming']
        )
        self.placement_template_site.should_have_text(
            digital_test_data['site_mts_dsp_name']
        )
        self.placement_template_placement_type.should_have_text(
            digital_test_data['placement_type_din_name']
        )
        self.placement_template_buy_type.should_have_text(
            digital_test_data['buy_type_vcpm_name']
        )
        self.placement_template_channel.should_have_text(
            digital_test_data['channel_display_name']
        )
        self.placement_template_ad_format.should_have_text(
            digital_test_data['ad_format_adaptive_html_name']
        )
        self.placement_template_ad_size.should_have_text(
            digital_test_data['ad_size_1000x250_name']
        )
        self.placement_template_benchmark_metric_name.should_have_text(
            digital_test_data['ctr_metric_name'], metric_num='0'
        )
        self.placement_template_benchmark_metric_value.should_have_value(
            metric_value, metric_num='0'
        )

    def save_placement_template(self) -> None:
        """Сохранить шаблон размещения"""
        self.save_placement_template_btn.click()

    def get_back_from_placement_template_page(self) -> None:
        """Вернуться назад из страницы сценария размещения"""
        self.placement_template_back_btn.click()
        self.confirmation_dialog.confirm()

