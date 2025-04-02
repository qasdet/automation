from playwright.sync_api import Page
from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from helper.default_dates import (
    get_default_campaign_begin_date_for_ui,
    get_default_campaign_end_date_for_ui,
)
from user_office import constants


class DigitalPlacementComposition:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.placement_name = Input(
            page=page,
            locator='[data-testid="placement_name"]',
            name='Имя размещения',
        )
        self.placement_begin = Input(
            page, locator='[data-testid="placement_start_on"]', name='datenow'
        )
        self.placement_end = Input(
            page, locator='[data-testid="placement_finish_on"]', name='dateend'
        )
        self.site = DropDownList(
            page=page,
            locator='[data-testid="placement_site"]',
            name='Площадка',
        )
        self.seller = DropDownList(
            page=page,
            locator='[data-testid="placement_seller"]',
            name='Продавец',
        )
        self.placement_type = DropDownList(
            page=page,
            locator='[data-testid="placement_placement_type"]',
            name='Тип размещения'
        )
        self.placement_landing = DropDownList(
            page=page,
            locator='[data-testid="placement_landing"]',
            name='Выберите ссылку на лендинг',
        )
        self.placement_channel = DropDownList(
            page=page,
            locator='[data-testid="placement_channel"]',
            name='Выберите канал',
        )
        self.placement_buy_type = DropDownList(
            page=page,
            locator='[data-testid="placement_buy_type"]',
            name='Выберите тип ' 'закупки',
        )
        self.placement_ad_format = DropDownList(
            page=page,
            locator='[data-testid="placement_ad_format"]',
            name='Выбор формата',
        )
        self.placement_ad_size = DropDownList(
            page=page,
            locator='[data-testid="placement_size"]',
            name='Размер',
        )
        self.placement_switch_checkbox = Button(
            page=page,
            locator='[data-testid="placement_switch"]',
            name='Активный статус',
        )
        self.placement_publish_button = Button(
            page,
            locator='[data-testid="summary_button_publish"]',
            name="Публикация"
        )
        self.placement_platform = DropDownList(
            page,
            locator='[data-testid="placement_platform"]',
            name='Платформа'
        )
        self.platform_item = Input(
            page,
            locator="text='Десктоп'",
            name='Десктоп',
        )

    def check_default_placement_begin_date(self):
        """Проверка наличия дефолтного значения даты начала размещения"""
        self.placement_begin.should_have_value(
            get_default_campaign_begin_date_for_ui()
        )

    def check_default_placement_end_date(self):
        """Проверка наличия дефолтного значения даты завершения размещения"""
        self.placement_end.should_have_value(
            get_default_campaign_end_date_for_ui()
        )

    def input_placement_name(self, placement_name: str) -> None:
        """Ввод названия размещения
        Args:
            placement_name: Название размещения
        """
        self.placement_name.fill(value=placement_name, validate_value=True)

    def select_site(self, site_name: str) -> None:
        """Выбрать площадку
            Args:
                site_name: название площадки
        """
        self.site.select_item_by_text(site_name)

    def select_placement_type(self, placement_type_name: str) -> None:
        """Выбрать тип размещения
            Args:
                placement_type_name: название типа размещения
        """
        self.placement_type.select_item_by_text(placement_type_name)

    def select_landing(self, landing_link: str) -> None:
        """Добавить лендинг
            Args:
                landing_link: ссылка на лендинг
        """
        self.placement_landing.select_item_by_text(landing_link)

    def select_channel(self, channel_name: str) -> None:
        """Добавить канал
            Args:
                channel_name: название канала
        """
        self.placement_channel.select_item_by_text(channel_name)

    def select_buy_type(self, buy_type_name: str) -> None:
        """Добавить тип закупки
            Args:
                buy_type_name: название типа закупки
        """
        self.placement_buy_type.select_item_by_text(buy_type_name)

    def select_ad_format(self, ad_format_name: str) -> None:
        """Добавить формат
            Args:
                ad_format_name: название формата
        """
        self.placement_ad_format.select_item_by_text(ad_format_name)

    def select_ad_size(self, ad_size_name: str) -> None:
        """Добавить размер
            Args:
                ad_size_name: название размера
        """
        self.placement_ad_size.select_item_by_text(ad_size_name)

    def select_platform(self, platform_name: str) -> None:
        """Добавить платформу
            Args:
                platform_name: название платформы
        """
        self.placement_platform.select_item_by_text(platform_name)

    def fill_placement_composition_in_progress_status(self, digital_test_data: dict) -> None:
        """Создание размещения в статусе В работе
        Args:
            digital_test_data: массив тестовых данных
        """
        self.select_site(digital_test_data['site_mytarget_name'])
        self.check_default_placement_begin_date()
        self.check_default_placement_end_date()
        self.input_placement_name(digital_test_data['placement_name'])

    def fill_placement_composition_fields_for_completed_status(
            self, digital_test_data: dict
    ) -> None:
        """Создание размещения в статусе 'Заполнено'
        Args:
            digital_test_data: массив тестовых данных
        """
        self.select_site(digital_test_data['site_mts_dsp_name'])
        self.select_platform(digital_test_data['placement_platform_desktop_name'])
        self.select_landing(digital_test_data['landing_url'])
        self.select_buy_type(digital_test_data['buy_type_cpm_name'])
        self.check_default_placement_begin_date()
        self.check_default_placement_end_date()
        self.select_channel(digital_test_data['channel_display_name'])
        self.input_placement_name(digital_test_data['placement_name'])

    def create_placement_for_metrics_calculating(self) -> None:
        """Создать размещение для перехода на вкладку Метрики"""
        self.select_site()
        self.select_placement_type()
        self.check_default_placement_begin_date()
        self.check_default_placement_end_date()
        self.check_default_placement_begin_date()
        self.check_default_placement_end_date()
        self.select_landing()
        self.select_buy_type()
        self.select_ad_format()
        self.select_ad_size()
        self.select_platform()
        self.save_placement_btn.hover()
        self.save_placement_btn.click()
        self.metrics_tab.should_be_visible()
        self.metrics_tab.click()

    def check_placement_composition_retry(self, digital_test_data: dict) -> None:
        """
        Проверка повтора данных размещения перед переключением в статус Заполнено и сохранением
            Args:
                digital_test_data: массив тестовых данных
        """
        self.site.should_have_text(digital_test_data['site_mts_dsp_name'])
        self.placement_platform.should_have_text(digital_test_data['placement_platform_desktop_name'])
        self.placement_type.should_have_text(digital_test_data['placement_type_din_name'])
        self.placement_landing.should_have_text(digital_test_data['landing_url'])
        self.placement_buy_type.should_have_text(digital_test_data['buy_type_cpm_name'])
        self.check_default_placement_begin_date()
        self.check_default_placement_end_date()
        self.placement_channel.should_have_text(digital_test_data['channel_display_name'])
        self.placement_name.should_have_value(
            f'2_{digital_test_data["site_mts_dsp_name"].replace(" ", "")}_{digital_test_data["channel_display_name"]}_'
            f'{digital_test_data["buy_type_cpm_name"]}'
        )

    def check_filled_placement_form_in_excel_file(self, cell) -> None:
        """Проверка заполнения из Эксель шаблона
        Args:
            cell: данные из эксель шаблона
        """
        self.placement_channel.should_have_text(text=cell[0][0])
        self.seller.should_have_text(text=cell[0][1])
        self.site.should_have_text(text=cell[0][2])
        self.placement_ad_format.should_have_text(text=cell[2][0])
        self.placement_ad_size.should_have_text(text=cell[2][2])
        self.placement_begin.should_have_value(text=cell[3][1][:10])
        self.placement_end.should_have_value(text=cell[3][1][13:])
        self.placement_buy_type.should_have_text(text=cell[3][2])
        self.seller.should_have_text(text=cell[0][1])
        self.site.should_have_text(text=cell[0][2])