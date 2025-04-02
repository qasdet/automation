from playwright.sync_api import Page
from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title


class ProductCard:
    """Модель страницы карточка организации"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.save_button = Button(
            page,
            locator="[data-testid='product_card_save_button']",
            name='Сохранить',
        )
        self.cancel_button = Button(
            page,
            locator="[data-testid='product_card_cancel_button']",
            name='Отмена',
        )
        self.input_name = Input(
            self.page,
            locator="[data-testid='product_card_name']",
            name='Наименование',
        )
        self.input_naming = Input(
            self.page,
            locator="[data-testid='product_card_naming']",
            name='Нейминг',
        )
        self.organizations = DropDownList(
            self.page,
            locator="[data-testid='product_card_organizations']",
            name='Тип продукта',
        )
        self.type_product = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_type_product']",
            name='Тип продукта',
        )
        self.price_category = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_price_categories']",
            name='Ценовая категория',
        )
        self.brands = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_brands']",
            name='Бренды',
        )
        self.seasonalities = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_seasonalities']",
            name='Сезонность',
        )
        self.category = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_category']",
            name='Категория',
        )
        self.geographies = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_geographies']",
            name='География продукта',
        )
        self.purchase_frequencies = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_purchase_frequencies']",
            name='Частота покупок',
        )
        self.seasonality_values = DropDownList(
            self.page,
            locator="//div[@data-testid='product_card_seasonality_values']",
            name='Значение сезонности',
        )
        self.title = Title(
            self.page,
            locator="[data-testid='product_card_title']",
            name='Заголовок',
        )
        self.product_card_delete_button = Button(
            self.page,
            locator="[data-testid='product_card_delete_button']",
            name='Удалить'
        )

    def fill_product_name_field(self, name_value: str) -> None:
        """ Заполняет поле 'Наименование' """
        self.input_name.should_be_visible()
        self.input_name.fill(name_value)

    def click_delete_button_product_card(self) -> None:
        """ Нажимает кнопку 'Удалить' в карточке продукта """
        self.product_card_delete_button.should_be_visible()
        self.product_card_delete_button.click()

    def fill_all_fields(
        self,
        name: str,
        naming: str,
        type_product: str,
        price_category: str,
        seasonalities: str,
        category: str,
        geographies: str,
        purchase_frequencies: str,
        seasonality_values: str,
        organization: str,
    ) -> None:
        """Заполняем все поля формы
        Args:
            name: Наименование продукта
            naming: Нейминг продукта
            type_product: Тип продукта
            price_category: Ценовая категория
            seasonalities: Сезонность
            category: Категория
            geographies: География продукта
            purchase_frequencies: Частота покупок
            seasonality_values: Значение сезонности
            organization: Организация
        """
        self.organizations.select_item_by_text(organization)
        self.input_name.fill(name)
        self.input_naming.fill(naming)
        self.type_product.select_item_by_text(type_product)
        self.price_category.select_item_by_text(price_category)
        self.seasonalities.select_item_by_text(seasonalities)
        self.category.select_item_by_text(category)
        self.geographies.select_item_by_text(geographies)
        self.purchase_frequencies.select_item_by_text(purchase_frequencies)
        self.seasonality_values.select_item_by_text(seasonality_values)

    def save_product(self) -> None:
        """Сохранить продукт"""
        self.save_button.click()
        self.save_button.should_be_not_visible()
