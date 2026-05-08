from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.campaign.campaign_model import DigitalAboutCampaign


class AboutCampaignPage(BasePage):
    """
    Страница просмотра детальной информации о кампании (about campaign).

    Наследует функциональность от BasePage и представляет собой страницу
    с полной информацией о выбранной кампании, включая все настройки,
    статистику и связанные данные.

    Использование:
        >>> about_page = AboutCampaignPage(page)
        >>> about_page.digital_about_campaign.should_be_visible()

    Attributes:
        digital_about_campaign: Модель компонентов страницы About Campaign
                              (описание, настройки, статистика кампании)
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать страницу About Campaign.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
        """
        super().__init__(page=page)
        self.digital_about_campaign = DigitalAboutCampaign(page)
