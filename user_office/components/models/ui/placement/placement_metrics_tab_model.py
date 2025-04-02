from playwright.sync_api import Page
from controller.button import Button
from controller.input import Input
from controller.list_item import ListItem
from controller.drop_down_list import DropDownList
from helper.metric_calculator import MetricsCalculator


class DigitalPlacementMetrics(MetricsCalculator):
    def __init__(self, page: Page) -> None:
        self.page = page
        self.add_metrics_button_quantitative = Button(
            page=page,
            locator='[data-testid="placement_add_metrics_button_QUANTITATIVE"]',
            name='Добавить количественную метрику',
        )
        self.add_metric_price = Button(
            page=page,
            locator='[data-testid="placement_add_metrics_button_PRICE"]',
            name="Ценовые метрики"
        )
        self.quantitative_metric_name = DropDownList(
            page=page,
            locator='[data-testid="placement_name_metric__quantitative_{metric_num}"]',
            name='Список метрик',
        )
        self.quantitative_metric_value = Input(
            page=page,
            locator='[data-testid="placement_value_metric__quantitative_{metric_num}"]',
            name='Значение метрики',
        )
        self.benchmark_metric_name = DropDownList(
            page=page,
            locator='[data-testid="placement_name_metric__benchmarks_{metric_num}"]',
            name='Список метрик с типом Бенчмарк'
        )
        self.benchmark_metric_value = Input(
            page=page,
            locator='[data-testid="placement_value_metric__benchmarks_{metric_num}"]',
            name='Значение метрики с типом Бенчмарк'
        )
        self.metric_item = ListItem(
            page=page,
            locator='text="{name}"',
            name='Название выбраной метрики из списка',
        )
        self.price_metric_value = Input(
            page,
            locator="metrics.PRICE.{metric_num}.quantitative_metric_value",
            name='Значение ценовой метрики'
        )

    def select_quantitative_metric_name(self, metric_data: dict) -> None:
        """Добавить название метрики
        Args:
            metric_data: Словарь с данными метрики.
        """
        self.quantitative_metric_name.click(metric_num=metric_data['metric_num'])
        self.metric_item.click()

    def select_quantitative_metric_value(self, metric_data: dict) -> None:
        """Добавить значение метрики
        Args:
            metric_data: Словарь с данными метрики.
        """
        self.quantitative_metric_value.hover(metric_num=metric_data['metric_num'])
        self.quantitative_metric_value.fill(value=metric_data['metric_value'], metric_num=metric_data['metric_num'])

    def select_quantitative_metric(self, metric_data: dict) -> None:
        """Добавить количественную метрику
            Args:
                metric_data: Словарь с данными метрики.
        """
        self.add_metrics_button_quantitative.click()
        self.quantitative_metric_name.fill(
            metric_data['metric_name'], metric_num=metric_data['metric_num']
        )
        self.page.keyboard.press(key='Enter')
        self.quantitative_metric_value.click(metric_num=metric_data['metric_num'])
        self.quantitative_metric_value.fill(
            metric_num=metric_data['metric_num'], value=metric_data['metric_value']
        )

    def check_metric_name(self, metric_data: dict) -> None:
        """Проверка названия метрики
        Agrs:
            metric_data: Словарь с данными метрики.
        """
        self.quantitative_metric_name.should_have_text(
            text=metric_data['metric_name'], metric_num=metric_data['metric_num']
        )

    def check_metric_value(self, metric_data: dict) -> None:
        """Проверка значения метрики
        Args:
            metric_data: Словарь с данными метрики.
        """
        self.quantitative_metric_value.should_have_value(
            value=metric_data['metric_value'], metric_num=metric_data['metric_num']
        )

    def check_filled_metric(self, metric_data: dict):
        """
        Проверка заполненной метрики.
        Args:
            metric_data: Словарь с данными метрики.
        """
        self.check_metric_name(metric_data=metric_data)
        self.check_metric_value(metric_data=metric_data)

    def check_calculated_metric_by_row(self, row: int, value: str) -> None:
        """Проверка значения метрики
        Agrs:
            row: порядковый номер строки
            quantitative_metric_value: значение метрики
        """
        self.quantitative_metric_value.hover(row=row)
        self.quantitative_metric_value.should_have_value(value, row=row)

    def check_calculated_metrics_cpm_cpc_ctr(self) -> None:
        self.open_metrics_tab.click()
        self.add_metrics_button_quantitative.click()
        self.add_metric('Бюджет', MetricsCalculator.BUDGET, 0)
        self.add_metrics_button_quantitative.click()
        self.add_metrics_button_quantitative.click()
        self.add_metric('Показы', MetricsCalculator.IMPS, 1)
        self.save_placement_metric_btn.click()
        self.save_placement_metric_btn.click()
        self.check_calculated_metric_by_row(
            2, MetricsCalculator.formula_for_cpm()
        )
        self.add_metrics_button_quantitative.click()
        self.add_metric('Клики', MetricsCalculator.CLICKS, 3)
        self.save_placement_metric_btn.click()
        self.save_placement_metric_btn.click()
        self.check_calculated_metric_by_row(
            4, MetricsCalculator.formula_for_cpc()
        )
        self.check_calculated_metric_by_row(
            5, MetricsCalculator.formula_for_ctr()
        )
