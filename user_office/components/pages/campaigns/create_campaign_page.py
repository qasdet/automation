from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.campaign.campaign_model import DigitalCreateCampaign


class CreateCampaignPage(BasePage):
    """
    Страница создания новой кампании.

    Наследует функциональность от BasePage и представляет собой страницу
    с формой для создания новой кампании: заполнение параметров,
    настройка таргетинга, выбор дат и бюджета.

    Использование:
        >>> create_page = CreateCampaignPage(page)
        >>> create_page.digital_create_campaign.fill_name("Моя кампания")
        >>> create_page.digital_create_campaign.submit()

    Attributes:
        digital_create_campaign: Модель компонентов формы создания кампании
                              (поля ввода, кнопки, селекты)
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать страницу создания кампании.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
        """
        super().__init__(page=page)
        self.digital_create_campaign = DigitalCreateCampaign(page)
