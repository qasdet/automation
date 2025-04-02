import allure
import requests
import urllib3
from playwright.sync_api import Page, Response

from admin_office.components.models.ui.landing.landing_model import (
    LandingGeneral,
)
from admin_office.components.models.ui.side_bar.side_bar import SideBar

urllib3.disable_warnings(urllib3.connectionpool.InsecureRequestWarning)


class BasePage:
    """Основной контроллер для инициализации всех страниц"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.side_bar = SideBar(page)
        self.landing_model = LandingGeneral(page)

    def visit(self, url: str) -> Response.ok:
        with allure.step(f'Opening the url "{url}"'):
            r = requests.get(url, verify=False)
            return self.page.goto(r.url)

    def reload(self) -> Response.ok:
        with allure.step(f'Reloading page with url"{self.page.url}"'):
            return self.page.reload(wait_until='domcontentloaded')
