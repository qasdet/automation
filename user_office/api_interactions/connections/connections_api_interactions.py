import allure
import logging
import textwrap


from http_methods.post import post_request
from helper.subfield_selections import placement_tools_subfields, reporting_digital_connections_subfields


class ConnectionSettingsQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_report_connection_widget(self, mplan_id: str) -> dict:
        """Получить данные метрик в виджете по id
        Args:
            mplan_id: id медиаплана
        """
        query = {
            'variables': {
                'mplanID': mplan_id,
            },
            'query': """query ReportDigitalConnections($mplanID: ID!) {
                      reportDigitalConnections(mplanID: $mplanID) {
                        ...ReportFull
                        __typename
                      }
                    }"""
                     + reporting_digital_connections_subfields,
        }
        response = post_request(query=query, token=self.token)
        logging.info(
            f"API RESPONSE metric in connection widget {response['data']['reportDigitalConnections']['report']['label']}"
        )
        return response


class ConnectionSettingsMutationsAPI:
    def __init__(self, token):
        self.token = token

    def base_setup_placement_connection_settings(self, placement_id: str):
        """Базовое заполнение настроек подключений
                Args:
                    placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "data": [
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": None,
                        "publishMethod": "manual",
                        "type": "SITE"
                    },
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": None,
                        "type": "POSTCLICK"
                    },
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": None,
                        "type": "TRACKER"
                    },
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": None,
                        "type": "VERIFIER"
                    }
                        ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is base_setup_placement_connection_settings'
        ):
            logging.info(
                f'API RESPONSE: base_setup_placement_connection_settings: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def add_setup_placement_connection_settings_yandex_metric_post_click(
            self, placement_id: str, digital_test_data: dict
    ):
        """Базовое заполнение настроек подключений Яндекс
                Args:
                    placement_id: id размещения
                    digital_test_data: массив тестовых данных
        """
        mutation_query = {
            "variables":
            {
                "data": [
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": digital_test_data['itool_id_ym'],
                        "type": "POSTCLICK"
                    },
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": digital_test_data['itool_id_mts_dsp'],
                        "publishMethod": "manual",
                        "type": "SITE"
                    },
                    {
                        "gatherMethod": None,
                        "iToolID": None,
                        "trackingMethod": None,
                        "type": "TRACKER"
                    },
                    {
                        "gatherMethod": None,
                        "iToolID": None,
                        "type": "VERIFIER"
                    }
                ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_setup_placement_connection_settings_yandex_metric_post_click'
        ):
            logging.info(
                f'API RESPONSE: add_setup_placement_connection_settings_yandex_metric_post_click: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def add_setup_placement_connection_settings_yandex_metric_auto_post_click(
            self, placement_id: str, digital_test_data, integration_token
    ):
        """Базовое заполнение настроек подключений Яндекс метрика Автоматический сбор статистики
                Args:
                    placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "data": [
                        {
                            "gatherMethod": "MANUAL",
                            "iToolID": digital_test_data['itool_id_mts_dsp'],
                            "publishMethod": "manual",
                            "type": "SITE"
                        },
                        {
                            "counterID": "219235111",
                            "gatherMethod": "AUTO",
                            "iTokenID": integration_token,
                            "iToolID": digital_test_data['itool_id_ym'],
                            "type": "POSTCLICK"

                        },
                        {
                            "counterID": None,
                            "gatherMethod": "MANUAL",
                            "iTokenID": None,
                            "iToolID": None,
                            "type": "TRACKER"
                        },
                        {
                            "counterID": None,
                            "gatherMethod": "MANUAL",
                            "iTokenID": None,
                            "iToolID": None,
                            "type": "VERIFIER"
                        }
                    ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_setup_placement_connection_settings_yandex_metric_auto_post_click'
        ):
            logging.info(
                f'API RESPONSE: add_setup_placement_connection_settings_yandex_metric_auto_post_click: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def setup_connection_settings_with_only_one_source_manual(self, placement_id: str, digital_test_data: dict):
        """Базовое заполнение настроек подключений - Метод сборки статистики - Площадка - в ручную"""
        mutation_query = {
            "variables": {
                "data": [
                    {
                        "gatherMethod": "MANUAL",
                        "iToolID": digital_test_data['itool_id_mts_dsp'],
                        "publishMethod": "manual",
                        "type": "SITE"
                    }
                ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_setup_placement_connection_settings_yandex_metric_post_click'
        ):
            logging.info(
                f'API RESPONSE: add_setup_placement_connection_settings_yandex_metric_post_click: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def setup_connection_settings_with_only_one_post_click_tool_auto(self, placement_id: str,
                                                                     digital_test_data, integration_token_id):
        """Базовое заполнение настроек подключений - Post-Click автоматический сбор статистики в Яндекс метриках"""
        mutation_query = {
            "variables": {
                "data": [
                        {
                            "counterID": "219235111",
                            "gatherMethod": "AUTO",
                            "iTokenID": integration_token_id,
                            "iToolID": digital_test_data['itool_id_ym'],
                            "type": "POSTCLICK"
                        }
                    ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_setup_placement_connection_settings_yandex_metric_post_click'
        ):
            logging.info(
                f'API RESPONSE: add_setup_placement_connection_settings_yandex_metric_post_click: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def setup_connection_settings_with_source_manual_and_post_click_tool_auto(self, placement_id: str,
                                                                              digital_test_data, integration_token_id):
        """Базовое заполнение настроек подключений - Post-Click автоматический сбор статистикив Яндекс метриках и Площадка с ручным методом"""
        mutation_query = {
            "variables": {
                "data": [
                        {
                            "gatherMethod": "MANUAL",
                            "iToolID": digital_test_data['itool_id_mts_dsp'],
                            "publishMethod": "manual",
                            "type": "SITE"
                        },
                        {
                            "counterID": "219235111",
                            "gatherMethod": "AUTO",
                            "iTokenID": integration_token_id,
                            "iToolID": digital_test_data['itool_id_ym'],
                            "type": "POSTCLICK"

                        },
                        {
                            "counterID": None,
                            "gatherMethod": "MANUAL",
                            "iTokenID": None,
                            "iToolID": None,
                            "type": "TRACKER",
                            "trackingMethod": None
                        }
                    ],
                "id": placement_id
            },
            'query': """mutation PlacementToolsSave($id: ID!, $data: [PlacementToolData!]!) {
                              placementToolsSave(id: $id, data: $data) """ + placement_tools_subfields
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_setup_placement_connection_settings_yandex_metric_post_click'
        ):
            logging.info(
                f'API RESPONSE: add_setup_placement_connection_settings_yandex_metric_post_click: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response
