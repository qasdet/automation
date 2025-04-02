from playwright.sync_api import Page

from controller.button import Button
from controller.input import Input
from controller.list_item import ListItem
from helper.fixtures import generate_random_string, repeat_function
from user_office.components.models.ui.campaign.campaign_model import (
    DigitalCreateCampaign,
)


class CreateProduct(DigitalCreateCampaign):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name = Input(
            page,
            locator="[data-testid='create_product_name']",
            name='Имя продукта',
        )
        self.product_naming = Input(
            page,
            locator="[data-testid='create_product_naming']",
            name='Нейминг продукта',
        )
        self.deeplink = Input(
            page,
            locator="[data-testid='create_product_deep_link']",
            name='Ссылка',
        )
        self.product_type = ListItem(
            page,
            locator="[data-testid='create_product_type']",
            name='Тип продукта',
        )
        self.product_category = ListItem(
            page,
            locator="[data-testid='create_product_category']",
            name='Категория продукта',
        )
        self.product_price = ListItem(
            page,
            locator="[data-testid='create_product_price_categories']",
            name='Ценовая категория',
        )
        self.product_purchase = ListItem(
            page,
            locator="[data-testid='create_product_purchase_frequencies']",
            name='Частота покупок',
        )
        self.product_seasons = ListItem(
            page,
            locator="[data-testid='create_product_seasonalities']",
            name='Сезонность',
        )
        self.season_value = ListItem(
            page,
            locator="[data-testid='create_product_seasonalities_value']",
            name='Значение сезонности',
        )
        self.product_geo = ListItem(
            page,
            locator="[data-testid='create_product_geographies']",
            name='География',
        )
        self.btn_add_new_product = Button(
            page, locator='text="Новый продукт"', name='Новый продукт'
        )
        self.button_create = Button(
            page,
            locator="[data-testid='create_product_save_button']",
            name='Сохранить',
        )
        self.button_cancel = Button(
            page,
            locator="[data-testid='create_product_cancel_button']",
            name='Отменить',
        )

    def select_product_click(self):
        self.product.click()

    def create_campaign_with_50_products_in_rk(self, **data_campaign: dict):
        self.input_campaign_name(data_campaign['name'])
        self.input_campaign_naming(data_campaign['naming'])
        self.check_default_campaign_begin_date()
        self.check_default_campaign_end_date()
        self.select_client_click()
        self.select_brand_click()
        self.select_product_click()
        self.btn_add_new_product.click()

    # TODO: доработать методы для работы с клавиатурой и позже добавить проверки заполнения
    @repeat_function(50)
    def fill_name_campaing(self, **data_campaign: str):
        self.product_name.fill(data_campaign['name'])
        self.product_naming.fill(generate_random_string(7))
        self.deeplink.fill('https://yandex.ru/')
        self.product_type.click()
        self.page.keyboard.press('Enter')
        self.product_category.click()
        self.page.keyboard.press('Enter')
        self.product_price.click()
        self.page.keyboard.press('Enter')
        self.product_purchase.click()
        self.page.keyboard.press('Enter')
        self.product_seasons.click()
        self.page.keyboard.press('Enter')
        self.season_value.click()
        self.page.keyboard.press('Enter')
        self.page.keyboard.press('Escape')
        self.product_geo.click()
        self.page.keyboard.press('Enter')
        self.button_create.click()
        self.select_product_click()
        self.btn_add_new_product.click()
