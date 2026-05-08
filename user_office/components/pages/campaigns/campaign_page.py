from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.campaign.campaign_model import (
    DigitalCampaign,
    DigitalAboutCampaign,
)


class CampaignPage(BasePage):
    """
    Страница редактирования/просмотра кампании.

    Наследует функциональность от BasePage и представляет собой страницу
    для работы с кампанией: редактирование параметров, просмотр настроек,
    переход к детальной информации.

    Использование:
        >>> campaign_page = CampaignPage(page)
        >>> campaign_page.digital_campaign.fill_name("Новая кампания")

    Attributes:
        digital_campaign: Модель компонентов для работы с параметрами кампании
        digital_about_campaign: Модель компонентов страницы About (детальная информация)
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать страницу кампании.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
        """
        super().__init__(page=page)
        self.digital_campaign = DigitalCampaign(page)
        self.digital_about_campaign = DigitalAboutCampaign(page)
