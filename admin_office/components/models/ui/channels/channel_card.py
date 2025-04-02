from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title
from modals.dialog_modal import DialogModal


class ChannelCard:
    """Страница Карточка канала"""

    def __init__(self, page: Page) -> None:
        self.confirmation_dialog = DialogModal(page)
        self.create_button = Button(
            page=page,
            locator="//button[.='Создать']",
            name='Создать',
        )
        self.save_button = Button(
            page=page,
            locator="//button[.='Сохранить']",
            name='Сохранить',
        )
        self.cancel_button = Button(
            page=page,
            locator="//button[.='Отмена']",
            name='Отмена',
        )
        self.title = Title(
            page=page,
            locator='h2',
            name='Заголовок',
        )
        self.input_name = Input(
            page=page,
            locator="[name='name']",
            name='Название',
        )
        self.input_code = Input(page=page, locator="[name='code']", name='Код')
        self.input_naming = Input(
            page=page, locator="[name='naming']", name='Нейминг'
        )
        self.input_category_media_dropdown = DropDownList(
            page,
            locator="[class=' css-1tttbzh']",
            name='Категория медиа*',
        )
        self.input_category_media_field = Input(
            page,
            locator='#react-select-mediaType-input',
            name='Категория медиа*',
        )
        self.input_is_used_strat_plan = Input(
            page=page, locator="[name='isUsedBySplan']", name='Используется в страт-плане'
        )

    def fill_all_fields(
            self, **data_for_channel) -> None:
        """Заполняем все поля формы
        Args:
            name: Наименование
            code: Код
            naming: Нейминг
            media_type: Категория медиа
            is_used_by_splan: Используется ли в страт-плане
        """
        self.input_name.fill(data_for_channel['name'])
        self.input_code.fill(data_for_channel['code'])
        self.input_naming.fill(data_for_channel['naming'])
        self.input_category_media_dropdown.click()
        self.input_category_media_field.fill(data_for_channel['media_type'])
        self.input_category_media_dropdown.page.keyboard.press('Enter')
        self.input_is_used_strat_plan.click()

    def fill_required_fields(self, name, naming) -> None:
        """Заполняем обязательные поля формы
        Args:
            name: Имя
            naming: Нейминг
        """
        self.input_name.fill(name)
        self.input_naming.fill(naming)

    def click_save_channel_button(self) -> None:
        """Сохранить канал"""
        self.save_button.should_be_visible()
        self.save_button.click()

    def click_create_channel_button(self) -> None:
        """Создать канал """
        self.create_button.should_be_visible()
        self.create_button.click()

    def cancel_editing(self) -> None:
        """Сохранить канал"""
        self.cancel_button.click()
        self.confirmation_dialog.confirm()
        self.cancel_button.should_be_not_visible()
