import unittest

from playwright.sync_api import Page
from controller.input import Input


class DigitalPlacementTargeting(unittest.TestCase):
    def __init__(self, page: Page) -> None:
        super().__init__()
        self.page: Page = page
        self.base_targeting = Input(
            page=page,
            locator="[data-testid='targetings_baseTargeting']",
            name='Базовый таргетинг'
        )
        self.geo_targeting = Input(
            page=page,
            locator="[data-testid='targetings_geoTargeting']",
            name='Гео Тарогетинг'
        )

    def fill_placement_targetings(self, digital_test_data: dict) -> None:
        """Заполнить информацию о таргетингах
            Args:
                digital_test_data: массив тестовых данных
        """
        self.base_targeting.fill(digital_test_data['base_targeting_text'])
        self.geo_targeting.fill(digital_test_data['geo_targeting_text'])

    def check_filled_placement_targetings(self, digital_test_data: dict) -> None:
        """Проверка заполнения таргетингов размещения
            Args:
                digital_test_data: массив тестовых данных
        """
        base = self.page.get_by_test_id('targetings_baseTargeting').inner_html()
        self.assertEqual(first=base, second=digital_test_data['base_targeting_text'],
                         msg='Базовый Таргетинг не заполнен')
        geo = self.page.get_by_test_id('targetings_geoTargeting').inner_html()
        self.assertEqual(first=geo, second=digital_test_data['geo_targeting_text'], msg='Гео Таргетинг не заполнен')

    def check_filled_targeting_textarea_in_excel_file(self, cell) -> None:
        self.base_targeting.should_have_text(text=cell[1][0])
        self.geo_targeting.should_have_text(text=cell[1][1])
