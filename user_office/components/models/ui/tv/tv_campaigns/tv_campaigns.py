from playwright.sync_api import Page

from controller.button import Button
from controller.paging import Paging
from controller.tabbar import Tabbar
from controller.table_new import Table


class TVCampaigns:
    """Модель страницы ТВ кампаний"""

    def __init__(self, page: Page) -> None:
        self.create_button = Button(
            page=page,
            locator="[data-testid='campaigns_tv_create_button']",
            name='Добавить тв кампанию',
        )
        self.table = Table(
            page=page,
            locator="[data-testid='campaigns_tv_table']",
            name='Таблица тв кампаний',
        )
        self.paging = Paging(
            page=page, locator='.css-17in5p3', name='Пейджинг'
        )
        # TODO Временный локатор. Уточняю у разработчкиков
        self.tabbar = Tabbar(page=page, locator='.css-toju17', name='Меню')
        self.tv_tab = Button(
            page=page,
            locator="//a[.='ТВ кампании']",
            name='Вкладка ТВ кампании',
        )

    def open_the_tv_campaign_creation_form(self) -> None:
        """Открыть форму создания тв кампании"""
        self.create_button.click()

    def go_to_page_tv_campaign(self) -> None:
        """Перейти на вкладку ТВ кампании"""
        self.tv_tab.should_be_visible()
        self.tv_tab.click()
        self.create_button.should_be_visible()

    def check_visible_new_campaign_by_id(self, campaign_id: str) -> None:
        """Проверка отображаения новой записи по id
        Args:
            campaign_id: id тв кампании
        """
        self.table.should_be_visible_cell_by_text(text_cell=campaign_id)
