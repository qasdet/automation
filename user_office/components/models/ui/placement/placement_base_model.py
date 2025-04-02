from playwright.sync_api import Page
from controller.button import Button
from controller.title import Title
from user_office.components.models.ui.placement.placement_composition_tab_model import DigitalPlacementComposition
from user_office.components.models.ui.placement.placement_metrics_tab_model import DigitalPlacementMetrics
from user_office.components.models.ui.placement.placement_creatives_tab_model import DigitalPlacementCreatives
from user_office.components.models.ui.placement.placement_connections_tab_model import DigitalPlacementConnections
from user_office.components.models.ui.placement.placement_targeting_tab_model import DigitalPlacementTargeting
from user_office.components.models.ui.placement.placement_prices_tab_model import DigitalPlacementPrices
from user_office.components.models.ui.placement.placement_utm_tab_model import DigitalPlacementUTM
from db_stuff.db_interactions.sources_db_interactions import get_source_name_by_id
from db_stuff.db_interactions.sellers_db_interactions import get_seller_name_by_id
from db_stuff.db_interactions.buy_types_db_interactions import get_buy_type_name_by_id
from db_stuff.db_interactions.channels_db_interactions import get_channel_name_by_naming
from db_stuff.db_interactions.ad_formats_db_interactions import get_ad_format_name_by_id
from db_stuff.db_interactions.ad_sizes_db_interactions import get_ad_size_name_by_id
from helper.value_handler import value_handler
from helper.default_dates import (
    get_default_campaign_begin_date_for_ui,
    get_default_campaign_end_date_for_ui,
)


class DigitalPlacement:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.composition = DigitalPlacementComposition(page)
        self.metrics = DigitalPlacementMetrics(page)
        self.targeting = DigitalPlacementTargeting(page)
        self.creatives = DigitalPlacementCreatives(page)
        self.connections = DigitalPlacementConnections(page)
        self.prices = DigitalPlacementPrices(page)
        self.utm = DigitalPlacementUTM(page)
        self.placement_tab = Title(
            page, locator='#placement-tab-form', name='Вкладка размещения'
        )
        self.composition_tab = Button(
            page=page,
            locator='[data-testid="tab_composition"]',
            name='Вкладка Состав',
        )
        self.targeting_tab = Button(
            page=page,
            locator='[data-testid="tab_targeting"]',
            name='Вкладка Таргетинг',
        )
        self.prices_tab = Button(
            page=page,
            locator='[data-testid="tab_price"]',
            name='Вкладка Цены',
        )
        self.metrics_tab = Button(
            page=page,
            locator='[data-testid="tab_metrics"]',
            name='Вкладка Метрики',
        )
        self.utm_tab = Button(
            page=page,
            locator='[data-testid="tab_utm"]',
            name='Вкладка UTM',
        )
        self.connections_tab = Button(
            page=page,
            locator='[data-testid="tab_connections"]',
            name='Вкладка Подключения',
        )
        self.creatives_tab = Button(
            page=page,
            locator='[data-testid="tab_creative"]',
            name='Вкладка Креативы',
        )
        self.publication_button = Button(
            page=page,
            locator='[data-testid="summary_button_publish"]',
            name='Кнопка перехода к инструкции по публикации',
        )
        self.actions_button = Button(
            page=page,
            locator='[data-testid="summary_actions_button"]',
            name='Кнопка Действия',
        )
        self.back_to_mediaplan_button = Button(
            page,
            locator='[data-testid="placement_back"]',
            name='Возврат на страницу медиаплана',
        )
        self.save_button = Button(
            page=page,
            locator='[data-testid="placement_save"]',
            name='Кнопка сохранения размещения',
        )
        self.continue_button = Button(
            page=page,
            locator='[data-testid="placement_continue"]',
            name='Кнопка Продолжить',
        )

    def change_placement_status(self) -> None:
        self.page.get_by_role('checkbox').hover()
        self.page.get_by_role('checkbox').click()

    def click_utm_tab(self) -> None:
        """Кликнуть по вкладке 'UTM' """
        self.utm_tab.should_be_visible()
        self.utm_tab.click()

    def save_placement(self) -> None:
        self.save_button.should_be_visible()
        self.save_button.click()

    def continue_placement_create(self) -> None:
        self.continue_button.should_be_visible()
        self.continue_button.click()

    def back_to_mediaplan_page(self) -> None:
        """Назад на страницу медиаплана"""
        self.back_to_mediaplan_button.click()

    def create_placement_in_progress_status(self, digital_test_data: dict) -> None:
        """Создание размещения в статусе В работе
        Args:
            digital_test_data: массив тестовых данных
        """
        self.composition.fill_placement_composition_in_progress_status(digital_test_data)
        self.save_button.click()

    def create_placement_completed_status(
            self, digital_test_data: dict, metric_data: dict
    ) -> None:
        """Создание размещения в статусе 'Заполнено'
            Args:
                digital_test_data: массив тестовых данных
                metric_data: данные для метрики
        """
        self.composition.fill_placement_composition_fields_for_completed_status(digital_test_data)
        # text = self.page.get_by_role(role='alert').all_inner_texts()
        # assert text == ['Состав размещения успешно сохранен', '']
        # TODO: https://jira.mts.ru/browse/MDP-6511
        self.continue_placement_create()
        self.targeting.fill_placement_targetings(digital_test_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.metrics.select_quantitative_metric(metric_data=metric_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.continue_placement_create()
        self.continue_placement_create()
        #self.continue_placement_create()
        self.save_placement()
        self.change_placement_status()

    def accept_placement_data_to_retry(self, digital_test_data: dict, metric_data: dict) -> None:
        """
        Проверка данных повторяемого размещения перед сохранением.
            Args:
                digital_test_data: массив тестовых данных
                metric_data: данные метрики
        """
        self.composition.check_placement_composition_retry(digital_test_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.targeting.check_filled_placement_targetings(digital_test_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.metrics.check_filled_metric(metric_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.continue_placement_create()
        self.save_placement()

    def check_retried_placement_data(self, digital_test_data: dict, metric_data: dict) -> None:
        """
        Проверка данных повтора размещения.
            Args:
                digital_test_data: массив тестовых данных
                metric_data: данные метрики
        """
        self.composition.check_placement_composition_retry(digital_test_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.targeting.check_filled_placement_targetings(digital_test_data)
        self.continue_placement_create()
        self.continue_placement_create()
        self.metrics.check_filled_metric(metric_data)

    def create_placement_targetings(self, digital_test_data: dict) -> None:
        """Заполнить информацию о таргетингах
            Args:
                digital_test_data: массив тестовых данных
        """
        self.targeting.fill_placement_targetings(digital_test_data['base_targeting_text'])
        self.save_button.click()

    def create_connection_yandex_direct(self) -> None:
        """Заполнение полей настроек подключения. Яндекс Директ, Post-click tool Яндекс Метрика"""
        self.connections.fill_all_fields_yandex_direct()
        self.save_button.click()

    def create_connection_post_click_appsflyer(self) -> None:
        """Заполнение полей настроек подключения. Post-click tool AppsFlyer"""
        self.connections.fill_all_fields_post_click_appsflyer()
        self.save_button.click()

    def check_placement_from_templates_dictionary(
            self, digital_test_data: dict, metrics_data: dict
    ) -> None:
        """Метод проверяет созданное из справочников шаблонов размещение
            Args:
                digital_test_data: массив тестовых данных
                    digital_test_data['source_id_mts_dsp']: id площадки
                    digital_test_data['seller_id_mts']: id продавца
                    digital_test_data['placement_type_din']: название типа размещения
                    digital_test_data['buy_type_id']: id типа покупки
                    digital_test_data['channel_naming']: нейминг канала
                    digital_test_data['ad_format_id']: id формата
                    digital_test_data['ad_size_id']: id размера
                metrics_data: массив данных добавленных метрик
        """
        self.placement_tab.should_be_visible()
        self.composition.site.should_have_text(get_source_name_by_id(digital_test_data['source_id_mts_dsp']))
        self.composition.seller.should_have_text(get_seller_name_by_id(digital_test_data['seller_id_mts']))
        self.composition.placement_type.should_have_text(digital_test_data['placement_type_din'])
        self.composition.placement_buy_type.should_have_text(get_buy_type_name_by_id(digital_test_data['buy_type_id']))
        self.composition.placement_begin.should_have_value(get_default_campaign_begin_date_for_ui())
        self.composition.placement_end.should_have_value(get_default_campaign_end_date_for_ui())
        self.composition.placement_name.should_have_value(
            '2_' + get_source_name_by_id(digital_test_data['source_id_mts_dsp']).replace(' ', '') + '_' \
            + get_channel_name_by_naming(digital_test_data['channel_naming']) + '_' \
            + get_buy_type_name_by_id(digital_test_data['buy_type_id']) + '_' \
            + get_ad_format_name_by_id(digital_test_data['ad_format_id']).replace(' ', '')
        )
        self.composition.placement_channel.should_have_text(get_channel_name_by_naming(digital_test_data['channel_naming']))
        self.composition.placement_ad_format.should_have_text(get_ad_format_name_by_id(digital_test_data['ad_format_id']))
        self.composition.placement_ad_size.should_have_text(get_ad_size_name_by_id(digital_test_data['ad_size_id']))
        self.metrics_tab.click()
        self.metrics.benchmark_metric_name.should_have_text(
            metrics_data['data']['placementMetrics']['metrics'][0]['metric']['name'], row=0
        )
        self.metrics.benchmark_metric_value.should_have_value(
            value_handler(
                int(metrics_data['data']['placementMetrics']['metrics'][0]['quantitative_metric_value'])
            ), row=0
        )
        self.metrics.benchmark_metric_name.should_have_text(
            metrics_data['data']['placementMetrics']['metrics'][1]['metric']['name'], row=1
        )
        self.metrics.benchmark_metric_value.should_have_value(
            metrics_data['data']['placementMetrics']['metrics'][1]['quantitative_metric_value'], row=1
        )
        self.metrics.benchmark_metric_name.should_have_text(
            metrics_data['data']['placementMetrics']['metrics'][2]['metric']['name'], row=2
        )
        self.metrics.benchmark_metric_value.should_have_value(
            metrics_data['data']['placementMetrics']['metrics'][2]['quantitative_metric_value'], row=2
        )

    def clicking_in_tab_targeting(self):
        self.targeting_tab.click()