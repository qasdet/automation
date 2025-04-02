import logging
import textwrap
import allure

from http_methods.post import post_request


class UsersQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_all_list_users(self):
        """Метод возвращает список пользователей внутри организации по токену"""
        query = {
            'query': 'query profiles '
                     '{profiles {user {id login email phone status} '
                     'person { name surname middleName}}}'
        }
        responses = post_request(query=query, token=self.token)['data']['profiles']
        response = []
        for person in responses:
            response.append(
                {
                    "id": person["user"]["id"],
                    "login": person["user"]["login"],
                    "email": person["user"]["email"],
                    "phone": person["user"]["phone"],
                    "status": person["user"]["status"],
                    "name": person["person"]["name"],
                    "surname": person["person"]["surname"],
                    "middleName": person["person"]["middleName"],
                }
            )
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is get_all_list_users'
        ):
            logging.info(
                f'API RESPONSE: get users list by organization: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response
