import allure
import httpx
from playwright.sync_api import Page, Response
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from admin_office.components.models.ui.landing.landing_model import (
    LandingGeneral,
)
from user_office.components.models.ui.authorization.authorization import (
    AuthorizeUserOffice,
)
from user_office.components.models.ui.campaign.campaign_model import (
    DigitalAboutCampaign,
    DigitalCampaign,
    DigitalCampaignsList,
    DigitalCreateCampaign,
)
from user_office.components.models.ui.conversion.conversion import Conversion
from user_office.components.models.ui.fileUpload.upload import UploadExcel
from user_office.components.models.ui.health_check.health_user_office import (
    HealthUserOffice,
)
from user_office.components.models.ui.mediaplan.mediaplan_model import (
    DigitalCreateMediaplan,
    DigitalExportMP,
    DigitalMediaplan,
    DigitalMplanAnalytics
)
from user_office.components.models.ui.navbar.navbar import Navbar
from user_office.components.models.ui.product.product import CreateProduct
from user_office.components.models.ui.reporting.reporting import Reporting
from user_office.components.models.ui.strat_plan.specific_strat_plan import (
    StratPlanSpecific,
)
from user_office.components.models.ui.strat_plan.strat_plan_general import (
    StratPlanGeneral,
)
from user_office.components.models.ui.placement.placement_base_model import DigitalPlacement
from user_office.components.models.ui.instructions_for_pubclications.instruction import (
    InstructionsForPublications
)
from user_office.components.models.ui.dictionaries_page.dictionaries import Dictionaries, PlacementTemplate
from user_office.components.models.ui.analitycs_page.analitycs import AnalitycsPage
disable_warnings(InsecureRequestWarning)

"""Основной контроллер для инициализации всех страниц"""


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.navbar = Navbar(page)
        self.user_office = AuthorizeUserOffice(page)
        self.analitycs_page = AnalitycsPage(page)
        self.health_user_office = HealthUserOffice(page)
        self.digital_campaign = DigitalCampaign(page)
        self.digital_campaigns_list = DigitalCampaignsList(page)
        self.digital_create_campaign = DigitalCreateCampaign(page)
        self.digital_about_campaign = DigitalAboutCampaign(page)
        self.digital_mediaplan = DigitalMediaplan(page)
        self.digital_create_mediaplan = DigitalCreateMediaplan(page)
        self.digital_export_mp = DigitalExportMP(page)
        self.digital_placement = DigitalPlacement(page)
        self.digital_placement_template = PlacementTemplate(page)
        self.create_conversion = Conversion(page)
        self.create_product_in_rk = CreateProduct(page)
        self.strat_plan_general = StratPlanGeneral(page)
        self.specific_strat_plan = StratPlanSpecific(page)
        self.import_excel = UploadExcel(page)
        self.reporting = Reporting(page)
        self.landing_model = LandingGeneral(page)
        self.instructions_for_publications = InstructionsForPublications(page)
        self.dictionaries_page = Dictionaries(page)
        self.digital_mediaplan_analytics = DigitalMplanAnalytics(page)

    def visit(self, url: str) -> Response.ok:
        with allure.step(title=f'Opening the url "{url}"'):
            with httpx.Client(http2=True, verify=False) as client:
                r = client.get(url=url)
            return self.page.goto(url=str(r.url), wait_until='domcontentloaded')

    def reload(self) -> Response.ok:
        with allure.step(f'Reloading page with url"{self.page.url}"'):
            return self.page.reload(wait_until='domcontentloaded')
