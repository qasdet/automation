import allure
import logging
import random
import textwrap

from random import randint
from http_methods.post import post_request
from helper.default_dates import get_default_campaign_begin_date_for_api, get_default_campaign_end_date_for_api
from helper.subfield_selections import placement_subfields, fragment_all_placement, metrics_and_conversions_subfields
from pathlib import Path

this_dir = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename=f"{this_dir}/api.log",
    filemode="w",
)


class PlacementQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_placement_by_id(self, placement_id: str):
        """Поиск данных размещения по id
        Args:
            placement_id: id размещения
        """
        query = {
            "variables": {
                "id": placement_id,
            },
            "query": """query Placements($id: ID!) {
                        placements(id: $id) {
                            id
                                status {
                                id
                                name
                                code
                            }
                        }
                    }""",
        }
        response = post_request(query=query, token=self.token)
        logging.info(
            f'API RESPONSE GET placement id: {textwrap.shorten(str(response), width=80, placeholder="...")}'
        )
        return response

    def get_data_from_placements(self, placement_id: str) -> dict:
        """Отправка запроса на сервер для получения некоторых данных по размещению
        Args:
            placement_id: уникальный идентификатор рекламной кампании
        Returns:
            Возвращает часть данных о размещении
        """
        query = {
            'operation_name': 'Placements',
            'variables': {'id': f'{placement_id}'},
            'query': 'query Placements($id: ID!) {placements(id: $id) {name naming site {name seller {name}}}}',
        }
        result = post_request(query, token=self.token)
        return result['data']

    def get_all_placement_id_mplan(self, mplan_id: str):
        """Получить все размещения в рамках медиаплана
            Args:
                mplan_id: id медиаплана
            Returns:
                id всех размещений в рамках медиаплана
        """
        query = {
            'variables': {
                "slice": {
                    "limit": 11,
                    "offset": 0
                },
                "filter": {
                    "channelCode": {
                        "codes": [
                            "DIS"
                        ],
                        "isEmpty": False
                    },
                    "mplanIDs": [
                        mplan_id
                    ]
                }
            },

            "query": """query PlacementsForMediaplan($placementID: ID, $filter: PlacementFilter, $slice: ListSlice) {
                              placements(id: $placementID, filter: $filter, slice: $slice) {
                                ...PlacementForMediaplan
                                __typename
                              }
                            }""" + fragment_all_placement
        }
        response = post_request(query=query, token=self.token)
        logging.info(f'API RESPONSE {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def get_metrics_and_conversions(self, mplan_id: str, placement_id: str):
        """Получить метрики и конверсии размещения
        Args:
            mplan_id: id медиаплана
            placement_id: id размещения
        Returns:
            Данные о наличии добавленных метриках и конверсиях"""
        query = {
            "variables": {
                "mediaplanID": mplan_id,
                "placementID": placement_id
            },
            "query": """query MetricsAndConversions($placementID: ID!, $mediaplanID: ID!) {
                            placementMetrics(placementID: $placementID) """
                     + metrics_and_conversions_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is get_metrics_and_conversions'
        ):
            logging.info(
                f'API RESPONSE: get_metrics_and_conversions  '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response


class PlacementMutationsAPI:
    def __init__(self, token):
        self.token = token

    def create_placement_part_mts_dsp(self, mplan_id: str, digital_test_data: dict):
        """Создание размещения. Заполнены основные поля
        Args:
        mplan_id: id медиаплана
        digital_test_data: словарь тестовых данных
        """
        mutation_query = {
            "variables": {
                "data": {
                    "adFormatID": digital_test_data["ad_format_id"],
                    "adSizes": digital_test_data["ad_size_id"],
                    "buyTypeID": digital_test_data["buy_type_id"],
                    "channelCode": "DIS",
                    "landingURL": "https://yandex.ru",
                    "mplanID": mplan_id,
                    "sellerID": digital_test_data["seller_id_mts"],
                    "siteID": digital_test_data["source_id_mts_dsp"],
                    "startOn": get_default_campaign_begin_date_for_api(),
                    "finishOn": get_default_campaign_end_date_for_api(),
                    "name": digital_test_data["placement_name"],
                    "placementType": "DYNAMIC",
                    "platforms": ["MOBILE"],
                }
            },
            "query": """mutation PlacementCreate($data: PlacementData!) {
                                  placementCreate(data: $data) """
                     + placement_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is create_placement_part_mts_dsp'
        ):
            logging.info(
                f'API RESPONSE CREATE placement part mts dsp: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def create_placement_part_mts_dsp_add_random_channel(
            self, mplan_id: str, digital_test_data: dict
    ):
        """Создание размещения. Заполнены основные поля
        Args:
        mplan_id: id медиаплана
        digital_test_data: словарь тестовых данных
        channel: список каналов для рандомного заполнения в размещении
        """
        channel = ["DIS", "article"]
        mutation_query = {
            "variables": {
                "data": {
                    "adFormatID": digital_test_data["ad_format_id"],
                    "adSizes": digital_test_data["ad_size_id"],
                    "buyTypeID": digital_test_data["buy_type_id"],
                    "channelCode": random.choice(channel),
                    "landingURL": "https://yandex.ru",
                    "mplanID": mplan_id,
                    "sellerID": digital_test_data["seller_id_mts"],
                    "siteID": digital_test_data["source_id_mts_dsp"],
                    "startOn": f"{get_default_campaign_begin_date_for_api()}T00:00:00.000Z",
                    "finishOn": f"{get_default_campaign_end_date_for_api()}T00:00:00.000Z",
                    "name": digital_test_data["placement_name"],
                    "placementType": "DYNAMIC",
                    "platforms": ["MOBILE"],
                }
            },
            "query": """mutation PlacementCreate($data: PlacementData!) {
                            placementCreate(data: $data) """
                     + placement_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is create_placement_part_mts_dsp_add_random_channel'
        ):
            logging.info(f"RESPONSE: create_placement_part_mts_dsp_add_random_channel {response}")
        return response

    def create_placement_part_yandex_direct(
            self, mplan_id: str, digital_test_data: dict
    ):
        """Создание размещения. Заполнены основные поля
        Args:
        mplan_id: id медиаплана
        digital_test_data: словарь тестовых данных
        """
        mutation_query = {
            "variables": {
                "data": {
                    "adFormatID": digital_test_data["ad_format_id"],
                    "adSizes": digital_test_data["ad_size_id"],
                    "buyTypeID": digital_test_data["buy_type_id"],
                    "channelCode": "DIS",
                    "landingURL": "https://yandex.ru",
                    "mplanID": mplan_id,
                    "sellerID": digital_test_data["seller_id_ya"],
                    "siteID": digital_test_data["source_id_yd"],
                    "startOn": get_default_campaign_begin_date_for_api(),
                    "finishOn": get_default_campaign_end_date_for_api(),
                    "name": digital_test_data["placement_name"],
                    "placementType": "DYNAMIC",
                    "platforms": ["MOBILE"],
                }
            },
            "query": """mutation PlacementCreate($data: PlacementData!) {
                            placementCreate(data: $data) """
                     + placement_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that'
                      f' {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'create_placement_part_yandex_direct'
        ):
            logging.info(
                f'API RESPONSE CREATE placement part yandex direct: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def add_placement_metric_budget(self, placement_id: str):
        """Добавление метрики Бюджет
        Args:
            placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "data": {
                    "conversionLinks": [],
                    "metrics": [
                        {
                            "isCalculated": True,
                            "metricCode": "BUDGET",
                            "value": str(randint(0, 1000000)),
                        }
                    ],
                },
                "placementID": placement_id,
            },
            "query": """mutation SaveMetricsAndConversions($placementID: ID!, $data: PlacementMetricListData!) {
                          placementMetricsSave(placementID: $placementID, data: $data) {
                            metrics {
                              id
                              __typename
                            }
                            __typename
                          }
                        }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is add_placement_metric_budget'
        ):
            logging.info(
                f'API RESPONSE ADD placement metric budget: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def add_placement_metrics_budget_bounces_vimpr_cr_conversions(
            self, placement_id: str, conversion_code: str
    ):
        """Добавление метрик Бюджет, Отказы, Показы(видимые), CR, Конверсии
        с фиксированными значениями
            Args:
                placement_id: id размещения
                conversion_code: id конверсии
            Returns:
                id добавленных метрик
        """
        mutation_query = {
            "variables": {
                "data": {
                    "conversionLinks": [
                        {
                            "isMain": False,
                            "mplanConversionID": conversion_code,
                            "metrics": [
                                {
                                    "isCalculated": False,
                                    "metricCode": "CR",
                                    "value": "99.99",
                                },
                                {
                                    "isCalculated": False,
                                    "metricCode": "CONV",
                                    "value": "9999",
                                },
                            ],
                        }
                    ],
                    "metrics": [
                        {
                            "isCalculated": False,
                            "metricCode": "BUDGET",
                            "value": "999999999.99",
                        },
                        {
                            "isCalculated": False,
                            "metricCode": "BOUNCES",
                            "value": "999",
                        },
                        {
                            "isCalculated": False,
                            "metricCode": "VIMPR",
                            "value": "999999",
                        },
                    ],
                },
                "placementID": placement_id,
            },
            "query": """mutation SaveMetricsAndConversions($placementID: ID!, $data: PlacementMetricListData!) {
                          placementMetricsSave(placementID: $placementID, data: $data) {
                            metrics {
                              id
                              __typename
                            }
                            __typename
                          }
                        }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is add_placement_metrics_budget_bounces_vimpr_cr_conversions'
        ):
            logging.info(
                f'API RESPONSE add_placement_metrics_budget_bounces_vimpr_cr_conversions: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def add_placement_metrics_budget_cpa_cr_conversions(
            self, placement_id: str, conversion_id: str
    ):
        """Добавление метрик
            CR, CPA,
            Бюджет,
            Сессии
        Конверсии:
             CPA - Ценовая метрика
             CR - Бенчмарк
             Количество конверсий - количественная метрика
        с фиксироваными значениями
            Args:
                placement_id: id размещения
                conversion_id: id конверсии
            Returns:
                id добавленных метрик
        """
        mutation_query = {
            "variables": {
                "data": {
                    "conversionLinks": [
                        {
                            "isMain": True,
                            "mplanConversionID": conversion_id,
                            "metrics": [
                                {
                                    "isCalculated": False,
                                    "metricCode": "CR",
                                    "value": "9000"
                                },
                                {
                                    "isCalculated": False,
                                    "metricCode": "CPA",
                                    "value": "7000"
                                },
                                {
                                    "isCalculated": True,
                                    "metricCode": "CONV",
                                    "value": "1"
                                }
                            ]
                        }
                    ],
                    "metrics": [
                        {
                            "isCalculated": True,
                            "metricCode": "BUDGET",
                            "value": "7000"
                        },
                        {
                            "isCalculated": True,
                            "metricCode": "SESSIONS",
                            "value": "0.01111111111111111153515462746099728974513709545135498046875"
                        }
                    ]
                },
                "placementID": placement_id,
            },
            "query": """mutation SaveMetricsAndConversions($placementID: ID!, $data: PlacementMetricListData!) {
                          placementMetricsSave(placementID: $placementID, data: $data) {
                            metrics {
                              id
                              __typename
                            }
                            __typename
                          }
                        }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'add_placement_metrics_budget_bounces_vimpr_cr_conversions'
        ):
            logging.info(
                f'API RESPONSE add_placement_metrics_budget_bounces_vimpr_cr_conversions: {textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def add_placement_metrics_from_db_budget_cpa_cr_conversions(
            self, placement_id: str, conversion_id: str
    ):
        """
        Ввиду отсутствия гибкости запросов через апи, сделана копия методы с запросов в БД,
        #TODO: продумать как вытаскивать айди конверсий по конкретному имени и передавать в запрос
        Добавление метрик
            CR, CPA,
            Бюджет,
            Сессии
        Конверсии:
             CPA - Ценовая метрика
             CR - Бенчмарк
             Количество конверсий - количественная метрика
        с фиксироваными значениями
            Args:
                placement_id: id размещения
                conversion_id: id конверсии выбирается из базы по имени
            Returns:
                id добавленных метрик
        """
        mutation_query = {
            "variables": {
                "data": {
                    "conversionLinks": [
                        {
                            "isMain": True,
                            "mplanConversionID": conversion_id,
                            "metrics": [
                                {
                                    "isCalculated": False,
                                    "metricCode": "CR",
                                    "value": "9000"
                                },
                                {
                                    "isCalculated": False,
                                    "metricCode": "CPA",
                                    "value": "7000"
                                },
                                {
                                    "isCalculated": True,
                                    "metricCode": "CONV",
                                    "value": "1"
                                }
                            ]
                        }
                    ],
                    "metrics": [
                        {
                            "isCalculated": True,
                            "metricCode": "BUDGET",
                            "value": "7000"
                        },
                        {
                            "isCalculated": True,
                            "metricCode": "SESSIONS",
                            "value": "0.01111111111111111153515462746099728974513709545135498046875"
                        }
                    ]
                },
                "placementID": placement_id,
            },
            "query": """mutation SaveMetricsAndConversions($placementID: ID!, $data: PlacementMetricListData!) {
                             placementMetricsSave(placementID: $placementID, data: $data) {
                               metrics {
                                 id
                                 __typename
                               }
                               __typename
                             }
                           }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is add_placement_metrics_budget_bounces_vimpr_cr_conversions'
        ):
            logging.info(
                f'API RESPONSE add_placement_metrics_budget_bounces_vimpr_cr_conversions: {textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def add_placement_benchmark_metrics_for_placement_template(self, placement_id: str):
        """Добавление метрик с типом Бенчмарк (Частота, CTR, VTR), которые переносятся из справочника шаблонов
           размещений
        Args:
            placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "data": {
                    "conversionLinks": [],
                    "metrics": [
                        {
                            "isCalculated": True,
                            "metricCode": "FREQ",
                            "value": "5600",
                        },
                        {
                            "isCalculated": True,
                            "metricCode": "CTR",
                            "value": "90",
                        },
                        {
                            "isCalculated": True,
                            "metricCode": "VTR",
                            "value": "70",
                        }
                    ],
                },
                "placementID": placement_id,
            },
            "query": """mutation SaveMetricsAndConversions($placementID: ID!, $data: PlacementMetricListData!) {
                          placementMetricsSave(placementID: $placementID, data: $data) {
                            metrics {
                              id
                              __typename
                            }
                            __typename
                          }
                        }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is add_placement_metric_budget'
        ):
            logging.info(
                f'API RESPONSE ADD placement metrics freq, ctr, vtr: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def approve_placement(self, mplan_id: str, placement_id: str | list):
        """Утверждение размещения
        Args:
            mplan_id: id медиаплана
            placement_id: id размещения
        Returns:
            id утвержденного размещения
        """
        mutation_query = {
            "variables": {
                "mplanID": mplan_id,
                "placementIDs": placement_id
            },
            "query": """mutation PlacementsApprove($mplanID: ID!, $placementIDs: [ID!]!) {
                        placementsApprove(mplanID: $mplanID, placementIDs: $placementIDs) {
                            id
                            __typename
                            }
                        }""",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is approve_placement'
        ):
            logging.info(
                f'API RESPONSE approve_placement: {textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def setup_placement_completed_status(self, placement_id: str):
        """Переключение статуса размещения на Заполнено
        Args:
            placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "id": placement_id,
            },
            "query": "mutation placementSetupComplete($id: ID!) {placementSetupComplete(id: $id)}",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is setup_placement_completed_status'
        ):
            logging.info(
                f'API RESPONSE SETUP COMPLETE STATUS placement: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response

    def setup_placement_published_status(self, placement_id: str):
        """Переключение статуса размещения на Опубликована
        Args:
            placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "id": placement_id,
            },
            "query": "mutation placementPublish($id: ID!) {placementPublish(id: $id)}",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is setup_placement_published_status'
        ):
            logging.info(
                f'API RESPONSE SETUP PUBLISH STATUS placement: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        match response.values():
            case "[{'placementPublish': True}]":
                return True
            case "":
                return AssertionError("Размещение не опубликовано", print(response))

    def delete_placement(self, placement_id: str):
        """Удаление размещения
        Args:
            placement_id: id размещения
        """
        mutation_query = {
            "variables": {
                "id": placement_id,
            },
            "query": "mutation placementDelete($id: [ID!]!) {placementDelete(id: $id)}",
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is delete_placement'
        ):
            logging.info(f"API RESPONSE DELETE placement {response}")
        return response
