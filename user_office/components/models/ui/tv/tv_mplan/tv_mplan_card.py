from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.title import Title
from user_office.components.models.ui.tv.tv_mplan.dialog_constraints import (
    ConstraintsProductTVModal,
)


class TVMplanCard:
    """Модель страницы ТВ медиаплана"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.constraints_dialog = ConstraintsProductTVModal(page=page)
        self.client_and_brand_info = Title(
            page=page,
            locator="[data-testid='mp-tv-client-and-product']",
            name='Название клиента и продукта',
        )
        self.product_info = Title(
            page=page,
            locator="[data-testid='mp-tv-product']",
            name='Название продукта',
        )
        self.goals = DropDownList(
            page=page, locator="[data-testid='mp-tv-goals']", name='Цель'
        )
        self.target_spoiler = Button(
            page=page,
            locator="[data-testid='mp-tv-target-spoiler']",
            name='Спроллер Целевая аудитория',
        )
        self.gender = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-target-gender']",
            name='Пол',
        )
        self.age = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-target-age']",
            name='Возраст',
        )
        self.income = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-target-income']",
            name='Доход',
        )
        self.region = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-target-region']",
            name='География',
        )

        self.employment = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-target-employment']",
            name='Занятость',
        )

        self.kids = DropDownList(
            page=page, locator="[data-testid='mp-tv-target-kids']", name='Дети'
        )

        self.add_constraints_btn = Button(
            page=page,
            locator="[data-testid='mp-tv-add-constraints-button']",
            name='Добавить задачи и ограничения продукта',
        )

        self.create_draft_button = DropDownList(
            page=page,
            locator="[data-testid='mp-tv-form-button-draft-save']",
            name='Сохранить черновик МП',
        )
        self.back_button = Button(
            page=page,
            locator="[data-testid='mp-tv-form-button-goback']",
            name='Вернуться назад',
        )

    def check_info_about_mp(self, **kwargs: str) -> None:
        """Проверяем, что клиент, бренд и продукт в карточке МП совпадает с РК
        Args:
             **kwargs: ожидаемая информация
        """
        self.client_and_brand_info.should_have_text(
            f"{kwargs.get('client')} | {kwargs.get('brand')}"
        )
        self.product_info.should_have_text(
            f"{kwargs.get('product')}{kwargs.get('code_product')}"
        )

    def fill_fields(self, full_field: bool = False, **kwargs: str) -> None:
        """Заполнить поля
        Args:
            full_field: если True, то заполняем указанными данными,
            иначе проверяем, что указано значение по умолчанию
            **kwargs: ожидаеммая информация
        """
        self.goals.select_item_by_text(kwargs.get('goals'))
        self.target_spoiler.click()
        if full_field:
            # Выбираем указанные значения
            self.gender.select_item_by_text(kwargs.get('gender'))
            self.age.select_item_by_text(kwargs.get('age'))
            self.income.select_item_by_text(kwargs.get('income'))
            self.region.select_item_by_text(kwargs.get('region'))
            self.employment.select_item_by_text(kwargs.get('employment'))
            self.kids.select_item_by_text(kwargs.get('kids'))
        else:
            # Проверяем, что значения казаны по умолчанию (Любой\Любая\Любые)
            self.gender.should_have_text(kwargs.get('gender'))
            self.age.should_have_text(kwargs.get('age'))
            self.income.should_have_text(kwargs.get('income'))
            self.region.should_have_text(kwargs.get('region'))
            self.employment.should_have_text(kwargs.get('employment'))
            self.kids.should_have_text(kwargs.get('kids'))

        self.open_tasks_and_constraints_dialog()
        self.save_tasks_and_constraints_dialog()

    def create_draft(self) -> None:
        """Сохранить черновик МП"""
        self.create_draft_button.click()
        self.client_and_brand_info.should_be_visible()

    def open_tasks_and_constraints_dialog(self) -> None:
        """Открыть диалог Задачи и ограничения продукта"""
        self.add_constraints_btn.click()
        self.constraints_dialog.check_dialog_visible()

    def save_tasks_and_constraints_dialog(self) -> None:
        """Сохранить Задачи и ограничения продукта"""
        self.constraints_dialog.confirm()
        self.constraints_dialog.confirm_button.should_be_not_visible()

    def check_mp_info_in_draft_status(self, **kwargs: str) -> None:
        """Проверяем, что информация о МП совпадает с указанной
        Args:
            **kwargs: ожидаеммая информация
        """
        self.goals.should_have_text(kwargs.get('goals'))
        self.target_spoiler.click()
        self.gender.should_have_text(kwargs.get('gender'))
        self.age.should_have_text(kwargs.get('age'))
        self.income.should_have_text(kwargs.get('income'))
        self.region.should_have_text(kwargs.get('region'))
        self.employment.should_have_text(kwargs.get('employment'))
        self.kids.should_have_text(kwargs.get('kids'))

    def go_to_back(self) -> None:
        """Вернуться назад"""
        self.back_button.click()
