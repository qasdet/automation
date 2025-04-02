from playwright.sync_api import Page
from controller.drop_down_list import DropDownList
from controller.button import Button
from controller.input import Input


class SourcesCard:
    """Модель страницы создания площадки"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.sources_name_field = Input(
            page=page,
            locator="[data-testid='sources_name']",
            name='Наименование',
        )
        self.sources_short_name_field = Input(
            page=page,
            locator="[data-testid='sources_short_name']",
            name='Краткое наименование',
        )
        self.sources_naming_field = Input(
            page=page,
            locator="[data-testid='sources_naming']",
            name='Нейминг',
        )
        self.sources_url_field = Input(
            page=page,
            locator="[data-testid='sources_url']",
            name='URL',
        )
        self.sources_code_field = Input(
            page=page,
            locator="[data-testid='sources_code']",
            name='Код',
        )
        self.adset_checkbox = Button(
            page=page,
            locator="[data-testid='sources_hasAdset']",
            name='Имеет Adset',
        )
        self.auto_gather_checkbox = Button(
            page=page,
            locator="[data-testid='sources_can_auto_gather']",
            name='Автоматический сбор статистики',
        )
        self.sources_publish_method_dropdown = DropDownList(
            page=page,
            locator="[data-testid='sources_publish_method']",
            name='Метод публикации',
        )
        self.sources_seller_by_default_dropdown = DropDownList(
            page=page,
            locator="[data-testid='sources_seller']",
            name='Продавец по умолчанию',
        )
        self.sources_status_dropdown = DropDownList(
            page=page,
            locator="[data-testid='sources_status']",
            name='Статус площадки',
        )
        self.sources_type_dropdown = DropDownList(
            page=page,
            locator="[data-testid='sources_type']",
            name='Тип',
        )
        self.sources_type_dropdown = DropDownList(
            page=page,
            locator="[data-testid='sources_type']",
            name='Тип',
        )
        self.sources_button_create = Button(
            page=page,
            locator="[data-testid='sources_button_create']",
            name='Создать',
        )
        self.sources_button_cancel = Button(
            page=page,
            locator="[data-testid='sources_button_cancel']",
            name='Отмена',
        )
        self.sources_sizes_button_add = Button(
            page=page,
            locator="[data-testid='sources_sizes_button_add']",
            name='Добавить формат - размер',
        )
        self.sources_remove_button_sizes = Button(
            page=page,
            locator="[data-testid='sources_remove_button_sizes']",
            name='Удалить формат - размер',
        )
        self.sources_format_sizes = DropDownList(
            page=page,
            locator="[data-testid='sources_format_sizes']",
            name='Формат (размер)',
        )
        self.sources_size = DropDownList(
            page=page,
            locator="[data-testid='sources_size']",
            name='Размер',
        )
        self.sources_buy_types_button_add = Button(
            page=page,
            locator="[data-testid='sources_buy_types_button_add']",
            name='Добавить формат - тип закупки',
        )
        self.sources_remove_button_buy_types = Button(
            page=page,
            locator="[data-testid='sources_remove_button_buy_types']",
            name='Удалить формат - тип закупки',
        )
        self.sources_format_buy_types = DropDownList(
            page=page,
            locator="[data-testid='sources_format_buy_types']",
            name='Формат (тип закупки)',
        )
        self.sources_buy_type = DropDownList(
            page=page,
            locator="[data-testid='sources_buy_type']",
            name='Тип закупки',
        )

    def fill_sources_name_field(self, name_value: str) -> None:
        self.sources_name_field.should_be_visible()
        self.sources_name_field.fill(name_value)

    def fill_sources_short_name_field(self, short_name_value: str) -> None:
        self.sources_short_name_field.should_be_visible()
        self.sources_short_name_field.fill(short_name_value)

    def fill_sources_naming_field(self, naming_value: str) -> None:
        self.sources_naming_field.should_be_visible()
        self.sources_naming_field.fill(naming_value)

    def fill_sources_url_field(self, url_value: str) -> None:
        self.sources_url_field.should_be_visible()
        self.sources_url_field.fill(url_value)

    def fill_sources_code_field(self, code_value: str) -> None:
        self.sources_code_field.should_be_visible()
        self.sources_code_field.fill(code_value)

    def click_sources_adset_checkbox(self) -> None:
        self.adset_checkbox.should_be_visible()
        self.adset_checkbox.click()

    def click_sources_auto_gather_checkbox(self) -> None:
        self.auto_gather_checkbox.should_be_visible()
        self.auto_gather_checkbox.click()

    def fill_sources_publish_method_dropdown(self, method_value="Ручной") -> None:
        self.sources_publish_method_dropdown.should_be_visible()
        self.sources_publish_method_dropdown.select_item_by_text(method_value)

    def fill_sources_seller_by_default_dropdown(self, seller_value="МТС") -> None:
        self.sources_seller_by_default_dropdown.should_be_visible()
        self.sources_seller_by_default_dropdown.select_item_by_text(seller_value)

    def fill_sources_status_dropdown(self, source_value="Активный") -> None:
        self.sources_status_dropdown.should_be_visible()
        self.sources_status_dropdown.select_item_by_text(source_value)

    def fill_sources_type_dropdown(self, type_value) -> None:
        self.sources_type_dropdown.should_be_visible()
        self.sources_type_dropdown.select_item_by_text(type_value)

    def click_sources_sizes_button_add(self) -> None:
        self.sources_sizes_button_add.should_be_visible()
        self.sources_sizes_button_add.click()

    def fill_sources_format_sizes(self, format_value='Adaptive HTML') -> None:
        self.sources_format_sizes.should_be_visible()
        self.sources_format_sizes.select_item_by_text(format_value)

    def fill_sources_size(self, size_value='1000x1000') -> None:
        self.sources_size.should_be_visible()
        self.sources_size.select_item_by_text(size_value)

    def click_sources_sizes_button_delete(self) -> None:
        self.sources_remove_button_sizes.should_be_visible()
        self.sources_remove_button_sizes.click()

    def click_sources_buy_types_button_add(self) -> None:
        self.sources_buy_types_button_add.should_be_visible()
        self.sources_buy_types_button_add.click()

    def fill_sources_format_buy_types(self, format_value='MobileAds') -> None:
        self.sources_format_buy_types.should_be_visible()
        self.sources_format_buy_types.select_item_by_text(format_value)

    def fill_sources_buy_type(self, buy_type_value='CPM') -> None:
        self.sources_buy_type.should_be_visible()
        self.sources_buy_type.select_item_by_text(buy_type_value)

    def click_sources_remove_button_buy_types(self) -> None:
        self.sources_remove_button_buy_types.should_be_visible()
        self.sources_remove_button_buy_types.click()

    def click_sources_button_create(self) -> None:
        self.sources_button_create.should_be_visible()
        self.sources_button_create.click()

    def click_sources_button_cancel(self) -> None:
        self.sources_button_cancel.should_be_visible()
        self.sources_button_cancel.click()

    def sources_fill_all_fields(self,
                                name: str,
                                short_name: str,
                                naming: str,
                                url: str,
                                code: str,
                                ) -> None:
        """Заполнить все поля разом
        Args:
            name: наименование площадки
            short_name: краткое наименование площадки
            naming: нейминг площадки
            url: адрес площадки
            code: код площадки
        """
        self.fill_sources_name_field(name)
        self.fill_sources_short_name_field(short_name)
        self.fill_sources_naming_field(naming)
        self.fill_sources_url_field(url)
        self.fill_sources_code_field(code)
        self.click_sources_adset_checkbox()
        self.click_sources_auto_gather_checkbox()
        self.fill_sources_publish_method_dropdown()
        self.fill_sources_seller_by_default_dropdown()
        self.fill_sources_status_dropdown()
        self.click_sources_sizes_button_add()
        self.fill_sources_format_sizes()
        self.fill_sources_size()
        self.click_sources_buy_types_button_add()
        self.fill_sources_format_buy_types()
        self.fill_sources_buy_type()
