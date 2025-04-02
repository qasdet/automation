from playwright.sync_api import Page
from controller.grid import Grid
from controller.tabbar import Tabbar
from controller.title import Title
from controller.button import Button
from controller.date_picker import DatePicker
from helper.default_dates import get_default_campaign_begin_date_for_ui, get_default_campaign_end_date_for_ui
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Reporting:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.main = Title(page=page, locator='main', name='main')
        self.report_date_begin = DatePicker(
            page=page,
            locator="//div[@data-testid='plan_fact_start_period']",
            name='Дата начала отчета',
        )
        self.report_date_end = DatePicker(
            page=page,
            locator="//div[@data-testid='plan_fact_end_period']",
            name='Дата конца отчета',
        )
        self.plan_fact_tabbar = Tabbar(
            page=page,
            locator="[data-testid='digital_analytics_tabbar_plan_fact']",
            name='1'
        )
        self.calendar_day = Button(
            page=page,
            locator="[data-testid='{date}']",
            name='День в календаре'
        )
        self.canvas = Grid(
            page=page,
            locator="//canvas[@data-testid='data-grid-canvas']",
            name='canvas'
        )
        self.analytics_title = Title(
            page=page,
            locator="[data-testid='plan_fact_title']",
            name='Заголовок Аналитика'
        )

    def check_default_begin_date(self) -> None:
        """Проверка дефолтной даты начала отчета"""
        self.report_date_begin.hover()
        self.report_date_begin.should_be_visible()
        self.report_date_begin.should_have_value(get_default_campaign_begin_date_for_ui())

    def check_default_end_date(self) -> None:
        """Проверка дефолтной даты конца отчета"""
        self.report_date_end.hover()
        self.report_date_end.should_be_visible()
        self.report_date_end.should_have_value(get_default_campaign_end_date_for_ui())

    def check_calendar(self) -> None:
        """Проверка работоспособности календаря дейт-пикера, смена дат начала и завершения отчета.
           Проверка отображения новых дат в дейт-пикерах
           Новая дата начала: + 3 дня от дефолтной даты начала
           Новая дата завершения: - 3 от дефолтной даты завершения
        """
        default_begin_date = datetime.strptime(get_default_campaign_begin_date_for_ui(), '%d.%m.20%y')
        new_begin_date = (default_begin_date + relativedelta(days=+3)).strftime('%d.%m.20%y')
        default_end_date = datetime.strptime(get_default_campaign_end_date_for_ui(), '%d.%m.20%y')
        new_end_date = (default_end_date + relativedelta(days=-3)).strftime('%d.%m.20%y')
        self.report_date_begin.click()
        self.page.get_by_role("button", name="Previous Month").click()
        self.calendar_day.click(date=new_begin_date)
        self.report_date_end.click()
        self.calendar_day.click(date=new_end_date)
        self.analytics_title.click()
        self.report_date_begin.should_have_value(new_begin_date)
        self.report_date_end.should_have_value(new_end_date)

    def check_reporting_page(self) -> None:
        """Основная UI проверка страницы отчета план-факт"""
        self.page.reload()
        self.main.should_be_visible()
        self.canvas.should_be_visible()
        self.analytics_title.should_be_visible()
        self.plan_fact_tabbar.should_be_visible()
        self.check_default_begin_date()
        self.check_default_end_date()
        self.check_calendar()
        self.canvas.should_be_visible()
