import logging
import textwrap
import allure

from http_methods.post import post_request


class CreativesQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_creative_frames_from_specific_placement(self, placement_id) -> dict:
        """Получение списка рамок креативов для конкретного размещения
                Args:
                    placement_id: уникальный номер размещения
                Returns:
                    Возвращает словарь с результатом
        """
        get_creative_frames_query = {
            'operation_name': 'placementCreativeFrames',
            'variables': {'placementID': f'{placement_id}'},
            'query': 'query placementCreativeFrames($placementID: ID!)'
                     ' {placementCreativeFrames(placementID: $placementID) {id name naming}}'
        }
        response = post_request(query=get_creative_frames_query,
                                token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is '
                      f'creative frames for the placement exist'
        ):
            logging.info(
                f'API RESPONSE: creative frames: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}')
        return response

    def get_creatives_from_specific_placement(self, placement_id) -> dict:
        """Получение списка креативов для конкретного размещения
                Args:
                    placement_id: уникальный номер размещения
                Returns:
                    Возвращает словарь с результатом
        """
        get_creative_query = {
            'operation_name': 'placementCreatives',
            'variables': {'placementID': f'{placement_id}'},
            'query': 'query placementCreatives($placementID: ID!)'
                     ' {placementCreatives(placementID: $placementID) {id name naming}}'
        }
        response = post_request(query=get_creative_query,
                                token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is '
                      f'creatives for the placement exist'
        ):
            logging.info(
                f'API RESPONSE: creatives: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}')
        return response


class CreativesMutationsAPI:
    def __init__(self, token):
        self.token = token

    def create_creative_frame(self, campaign_id: str,
                              creative_frame_name_value: str,
                              creative_frame_naming_value: str,) -> dict:
        """Создание рамки креатива
                Args:
                    campaign_id: уникальный номер рекламной кампании
                    creative_frame_name_value: имя для рамки креатива
                    creative_frame_naming_value: нейминг для рамки креатива
                Returns:
                    Возвращает словарь с результатом
        """
        create_creative_frame_query = {
            'operation_name': 'creativeFrameCreate',
            'variables': {'data': {'campaignID': f'{campaign_id}',
                                   'name': f'{creative_frame_name_value}',
                                   'naming': f'{creative_frame_naming_value}'}},
            'query': 'mutation creativeFrameCreate($data: CreativeFrameCreateData!) '
                     '{creativeFrameCreate(data: $data) {id name naming}}'
        }
        response = post_request(query=create_creative_frame_query,
                                token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is '
                      f'creative frame created'
        ):
            logging.info(
                f'API RESPONSE: creative frame: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}')
        return response

    def delete_creative_frame(self, creative_frame_id_value: str) -> bool:
        """Удаление рамки креатива
                Args:
                    creative_frame_id_value: уникальный номер рамки креатива
                Returns:
                     Возвращает словарь с результатом
        """
        delete_creative_frame_query = {
            'operation_name': 'creativeFrameDelete',
            'variables': {
                'id': f'{creative_frame_id_value}'
            },
            'query': 'mutation creativeFrameDelete($id: ID!) {creativeFrameDelete(id: $id)}'
        }
        response = post_request(query=delete_creative_frame_query,
                                token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is '
                      f'creative frame deleted'
        ):
            logging.info(
                f'API RESPONSE: creative frame deleted: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}')
        return response['data']['creativeFrameDelete']

    def exclude_creative_frame(self, creative_frame_id_value: str) -> bool:
        """Исключение рамки креатива
                Args:
                    creative_frame_id_value: уникальный номер рамки креатива
                Returns:
                     Возвращает словарь с результатом
        """
        exclude_creative_frame_query = {
            'operation_name': 'creativeFrameExclude',
            'variables': {
                'id': f'{creative_frame_id_value}'
            },
            'query': 'mutation creativeFrameExclude($id: ID!) {creativeFrameExclude(id: $id)}'
        }
        response = post_request(query=exclude_creative_frame_query,
                                token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is '
                      f'creative frame excluded'
        ):
            logging.info(
                f'API RESPONSE: creative frame excluded: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}')
        return response['data']['creativeFrameExclude']
