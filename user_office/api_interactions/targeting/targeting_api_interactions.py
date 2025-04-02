import logging
import textwrap

from http_methods.post import post_request


class TargetingQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_targeting_descriptions_by_placement_id(self, placement_id: str):
        """Поиск базовых таргетингов по id медиаплана
                Args:
            mplan_id: id медиаплана
                Returns:
            Массив данных базовых таргетингов в рамках медиаплана
        """
        query = {
            "variables": {
                    "placementID": placement_id,
            },
            "query": """query PlacementTargeting($placementID: ID!) {
                          placementTargeting(placementID: $placementID) {
                            ...PlacementTargeting
                            __typename
                          }
                        }
                        
                        fragment PlacementTargeting on PlacementTargeting {
                          targetAudience
                          targetGeo
                          __typename
                        } """
        }
        response = post_request(query=query, token=self.token)
        logging.info(
            f'API RESPONSE get targeting descriptions: {textwrap.shorten(str(response), width=80, placeholder="...")}'
        )
        return response


class TargetingMutationsAPI:
    def __init__(self, token):
        self.token = token

    def add_targeting_descriptions(self, placement_id: str):
        """Добавление базового таргетинга
        Args:
        placement_id: id размещения
        base_targeting_id: id базового таргетинга
        """
        mutation_query = {
            "variables": {
                "placementID": placement_id,
                "data": {
                    "targetAudience": "This is a description of base targeting",
                    "targetGeo": "This is a description of geo targeting",
                }
            },
            "query": """mutation PlacementTargetingSave($data: PlacementTargetingData!, $placementID: ID!) {
                          placementTargetingSave(data: $data, placementID: $placementID) {
                            ...PlacementTargeting
                            __typename
                          }
                        }
                        fragment PlacementTargeting on PlacementTargeting {
                          targetAudience
                          targetGeo
                          __typename
                        } """
        }
        response = post_request(query=mutation_query, token=self.token)
        logging.info(
            f'API RESPONSE ADD base targetings: {textwrap.shorten(str(response), width=80, placeholder="...")}'
        )
        return response
