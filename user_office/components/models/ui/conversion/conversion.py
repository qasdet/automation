import random

from playwright.sync_api import Page

from controller.button import Button
from controller.input import Input
from controller.list_item import ListItem
from helper.fixtures import repeat_function


class Conversion:
    def __init__(self, page: Page):
        self.create_conversion_btn = Button(
            page,
            locator='data-testid=placement_add_conversions_button',
            name='Добавить конверсию',
        )
        self.list_items_conversion = ListItem(
            page,
            locator='data-testid=placement_conversion_name_{number}',
            name='Имя конверсии',
        )
        self.new_btn_conversion = Button(
            page,
            locator='data-testid=conversions_add_conversion_{number}',
            name='Новая конверсия',
        )
        self.input_conversion = Input(
            page,
            locator="[name='mplanConversionName']",
            name='Введите название конверсии',
        )
        self.btn_save_conversion = Button(
            page,
            locator='[data-testid="dialog_confirm"]',
            name='Сохранить конверсию',
        )
        self.conversion_switch = Button(
            page=page,
            locator='[data-testid="conversions_main_switch_0"]',
            name='Тумблер',
        )
        self.placement_save_button = Button(
            page=page,
            locator='[data-testid="placement_save_button"]',
            name='Сохранить',
        )

    # TODO: метод здесь лежит временно - позже переложу в файл fixtures в папке helpers
    @staticmethod
    def generate(n):
        for i in range(n):
            yield i

    lstep = generate(20)

    def create_conversion(self, number: int):
        self.create_conversion_btn.click()
        self.list_items_conversion.click(number=number)
        self.new_btn_conversion.click(number=number)
        self.input_conversion.fill(
            value='Conversions1' + f'{random.randint(1, 9999)}'
        )
        self.conversion_switch.should_be_visible()
        self.btn_save_conversion.click()

    def save_placement(self):
        self.placement_save_button.click()

    @repeat_function(20)
    def create_20_conversion(self):
        self.create_conversion(number=next(self.lstep))
