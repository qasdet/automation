from urllib.parse import urlparse

from playwright.sync_api import Page

from controller.button import Button
from controller.date_picker import DatePicker
from controller.drop_down_list import DropDownList
from controller.title import Title


class StratPlanSpecific:
    """Модель страницы стратегического плана"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = Title(
            page,
            locator='data-testid=strategic_planning_title',
            name='Стратегический план',
        )
        self.client_dropdown_menu = DropDownList(
            page,
            locator='data-testid=strategic_planning_client',
            name='Клиент',
        )
        self.brand_dropdown_menu = DropDownList(
            page, locator='data-testid=strategic_planning_brand', name='Бренд'
        )
        self.product_dropdown_menu = DropDownList(
            page,
            locator='data-testid=strategic_planning_product',
            name='Продукт',
        )
        self.category_dropdown_menu = DropDownList(
            page,
            locator='data-testid=strategic_planning_category',
            name='Банки, финансовые услуги, кэшбэк',
        )
        self.campaign_goal = DropDownList(
            page,
            locator='data-testid=params_planning_goal',
            name='Цель кампании',
        )
        self.strategy_of_competitors_in_category = DropDownList(
            page,
            locator='data-testid' '=params_planning_competitor_strategies',
            name='Стратегия размещения конкурентов в категории',
        )
        self.audience = DropDownList(
            page,
            locator='data-testid=params_planning_audience',
            name='Широкая аудитория 14-44',
        )
        self.date_start = DatePicker(
            page,
            locator='data-testid=params_planning_start_period',
            name='дд.мм.гггг',
        )
        self.date_end = DatePicker(
            page,
            locator='data-testid=params_planning_end_period',
            name='дд.мм.гггг',
        )
        # self.sub_segments = SwitchButton(page, locator="", name="")
        self.knowledge_of_the_product_with_hint_by_audience = Button(
            page,
            locator='data-testid' '=smpProductKnowledgeID_10_50_label',
            name='Сложность коммуникации',
        )
        self.complexity_of_communication = Button(
            page,
            locator='data-testid=smpCommunicationID_m3_label',
            name='Знание продукта аудиторией с подсказкой',
        )
        self.calculate_button = Button(
            page,
            locator='data-testid=params_planning_audience_calculate_button',
            name='Рассчитать',
        )

    def click_choose_client_dropdown_menu(self, client_name):
        self.client_dropdown_menu.select_item_by_text(name_item=client_name)

    def click_choose_brand_dropdown_menu(self, brand_name):
        self.brand_dropdown_menu.select_item_by_text(name_item=brand_name)

    def click_choose_product_dropdown_menu(self, product_name):
        self.product_dropdown_menu.select_item_by_text(name_item=product_name)

    def click_choose_category_dropdown_menu(self, category_name):
        self.category_dropdown_menu.select_item_by_text(
            name_item=category_name
        )

    def click_choose_campaign_goal(self, campaign_goal_name):
        self.campaign_goal.select_item_by_text(name_item=campaign_goal_name)

    def click_choose_strategy_of_competitors_in_category(
        self, name_of_strategy_of_competitors_in_category
    ):
        self.strategy_of_competitors_in_category.select_item_by_text(
            name_item=name_of_strategy_of_competitors_in_category
        )

    def click_choose_audience(self, audience_name):
        self.audience.select_item_by_text(name_item=audience_name)

    def input_date_start(self, date_start_value):
        self.date_start.click()
        self.date_start.fill(value=date_start_value)

    def input_date_end(self, date_end_value):
        self.date_end.click()
        self.date_end.fill(value=date_end_value)

    def click_knowledge_of_the_product_with_hint_by_audience(
        self, name_of_knowledge_of_the_product_with_hint_by_audience
    ):
        self.knowledge_of_the_product_with_hint_by_audience.click(
            name_item=name_of_knowledge_of_the_product_with_hint_by_audience
        )

    def click_complexity_of_communication(self, complexity_of_communication):
        self.complexity_of_communication.click(
            name_item=complexity_of_communication
        )

    def click_calculate_button(self):
        self.calculate_button.click()

    def get_id_from_url(self):
        self.page.reload()
        strat_plan_url_with_id = self.page.url
        strat_plan_id = urlparse(strat_plan_url_with_id).path.split('/')[-1]
        return strat_plan_id

    def input_all_fields(self, **kwargs) -> None:
        """Заполняем все поля стратплана"""
        self.click_choose_client_dropdown_menu(kwargs['client']['name'])
        self.click_choose_brand_dropdown_menu(kwargs['brand']['name'])
        self.click_choose_product_dropdown_menu(kwargs['product']['name'])
        self.click_choose_category_dropdown_menu(
            kwargs['productCategory']['name']
        )
        self.click_choose_campaign_goal(kwargs['smpGoal']['name'])
        self.click_choose_strategy_of_competitors_in_category(
            kwargs['smpCompetitorStrategy']['name']
        )
        self.input_date_start(kwargs['dateStart'])
        self.input_date_end(kwargs['dateEnd'])
        self.click_choose_audience(kwargs['smpAudience']['name'])
        self.click_knowledge_of_the_product_with_hint_by_audience(
            kwargs['smpProductKnowledge']['name']
        )
        self.click_complexity_of_communication(
            kwargs['smpCommunication']['name']
        )
