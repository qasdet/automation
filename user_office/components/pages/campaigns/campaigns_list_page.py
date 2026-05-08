from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.campaign.campaign_model import DigitalCampaignsList


class CampaignsListPage(BasePage):
    """
    Страница со списком всех кампаний (campaigns list).

    Наследует функциональность от BasePage и представляет собой страницу
    для работы со списком кампаний: просмотр, поиск, фильтрация,
    навигация к конкретной кампании.

    Использование:
        >>> list_page = CampaignsListPage(page)
        >>> list_page.digital_campaigns_list.should_have_count(10)
        >>> list_page.digital_campaigns_list.click_campaign_by_name("Тестовая кампания")

    Attributes:
        digital_campaigns_list: Модель компонентов списка кампаний
                              (таблица, фильтры, пагинация)
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать страницу списка кампаний.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
        """
        super().__init__(page=page)
        self.digital_campaigns_list = DigitalCampaignsList(page)
