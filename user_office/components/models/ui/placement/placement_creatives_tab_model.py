from playwright.sync_api import Page
from controller.button import Button
from controller.input import Input
from controller.drop_down_list import DropDownList
from controller.tabbar import Tabbar


class DigitalPlacementCreatives:
    """"Описание элементов вкладки 'Креативы'"""

    def __init__(self, page: Page):
        self.page = page
        self.creatives_tab = Tabbar(
            page,
            locator="[data-testid='placement_creative_tab']",
            name="Вкладка с креативами",
        )
        self.creative_add_button = Button(
            page,
            locator="[data-testid='creatives_add_button']",
            name="Добавить креатив",
        )
        self.creative_create_button = Button(
            page,
            locator="[data-testid='creatives_creative_add']",
            name='Создать креатив',
        )
        self.creative_context_menu = Button(
            page,
            locator="[data-testid='creatives_creative_item_action_button']",
            name='Контекстное меню креатива',
        )
        self.open_creatives_list = DropDownList(
            page,
            locator="[data-testid='creatives_creative_frame']",
            name='Раскрыть список креативов',
        )
        self.creative_frame_create_button = Button(
            page,
            locator="[data-testid='creatives_creative_frame_add']",
            name='Создать рамку креатива',
        )
        self.creative_frame_name = Input(
            page,
            locator="[data-testid='creative_frame_form_name']",
            name='Название рамки креатива',
        )
        self.creative_frame_naming = Input(
            page,
            locator="[data-testid='creative_frame_form_naming']",
            name='Нейминг рамки креатива',
        )
        self.creative_form_frame = DropDownList(
            page,
            locator="[data-testid='creative_form_frame']",
            name='Название креативной рамки в меню создания креатива',
        )
        self.creative_form_adsize = DropDownList(
            page,
            locator="[data-testid='creative_form_adsize']",
            name='Размер креатива',
        )
        self.creative_frame_form_cancel = Button(
            page,
            locator="[data-testid='creative_frame_form_cancel']",
            name='Отменить создание рамки креатива',
        )
        self.creative_frame_form_submit = Button(
            page,
            locator="[data-testid='creative_frame_form_submit']",
            name='Добавить в размещение рамку креатива',
        )
        self.creative_form_name = Input(
            page,
            locator="[data-testid='creative_form_name']",
            name='Название креатива',
        )
        self.creative_form_naming = Input(
            page,
            locator="[data-testid='creative_form_naming']",
            name='Нейминг креатива',
        )
        self.creative_form_cancel = Button(
            page,
            locator="[data-testid='creative_form_cancel']",
            name='Отменить создание креатива',
        )
        self.creative_form_submit = Button(
            page,
            locator="[data-testid='creative_form_submit']",
            name='Добавить в размещение креатив',
        )
        self.general_creative_form_add_into_placement = Button(
            page,
            locator="[data-testid='dialog_confirm']",
            name='Добавить в размещение креатив',
        )
        self.general_creative_form_cancel = Button(
            page,
            locator="[data-testid='dialog_cancel']",
            name='Отменить добавление креатива',
        )

    def click_general_button_confirm(self) -> None:
        self.general_creative_form_add_into_placement.should_be_visible()
        self.general_creative_form_add_into_placement.click()

    def click_general_button_cancel(self) -> None:
        self.general_creative_form_cancel.should_be_visible()
        self.general_creative_form_cancel.click()

    def click_creative_frame_form_submit(self) -> None:
        self.creative_frame_form_submit.should_be_visible()
        self.creative_frame_form_submit.click()

    def click_creative_frame_form_cancel(self) -> None:
        self.creative_frame_form_cancel.should_be_visible()
        self.creative_frame_form_cancel.click()

    def click_create_creative_frame_button(self) -> None:
        self.creative_frame_create_button.should_be_visible()
        self.creative_frame_create_button.click()

    def fill_creative_frame_name_field(self, creative_frame_name_value: str) -> None:
        self.creative_frame_name.should_be_visible()
        self.creative_frame_name.click()
        self.creative_frame_name.fill(creative_frame_name_value)

    def fill_creative_frame_naming_field(self, creative_frame_naming_value: str) -> None:
        self.creative_frame_naming.should_be_visible()
        self.creative_frame_naming.click()
        self.creative_frame_naming.fill(creative_frame_naming_value)

    def click_creative_tab(self) -> None:
        self.creatives_tab.should_be_visible()
        self.creatives_tab.click()

    def click_add_creative_button(self) -> None:
        self.creative_add_button.should_be_visible()
        self.creative_add_button.click()

    def click_create_creative_button(self) -> None:
        self.creative_create_button.should_be_visible()
        self.creative_create_button.click()

    def choose_creative_form_frame(self, creative_frame_name: str) -> None:
        self.creative_form_frame.should_be_visible()
        self.creative_form_frame.click()
        self.creative_form_frame.page.get_by_role('option', name=creative_frame_name).click()

    def choose_creative_adsize(self, creative_adsize_value: str) -> None:
        self.creative_form_adsize.should_be_visible()
        self.creative_form_adsize.click()
        self.creative_form_adsize.page.get_by_role('option', name=creative_adsize_value).click()

    def fill_creative_name(self, creative_name_value: str) -> None:
        self.creative_form_name.should_be_visible()
        self.creative_form_name.click()
        self.creative_form_name.fill(creative_name_value)

    def fill_creative_naming(self, creative_naming_value: str) -> None:
        self.creative_form_naming.should_be_visible()
        self.creative_form_naming.click()
        self.creative_form_naming.fill(creative_naming_value)

    def click_creative_form_submit(self) -> None:
        self.creative_form_submit.should_be_visible()
        self.creative_form_submit.click()

    def click_dropdown_creative_frame(self) -> None:
        self.open_creatives_list.should_be_visible()
        self.open_creatives_list.click()

    def get_name_creative_frame(self, creative_frame_name_to_check) -> None:
        self.open_creatives_list.should_be_visible()
