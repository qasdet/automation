import pytest
import allure
import humps

from admin_office.api_interactions.clients.clients_api_interactions import (
    get_clients_api,
    create_client_admin_office,
    update_client,
    delete_client_by_id,
)
from admin_office.tests.api.dictionaries.clients.data_make_for_client import make_data_all_client_fields
from db_stuff.db_interactions.organizations_db_interactions import get_organization_id_by_name
from db_stuff.db_interactions.clients_db_interactions import (
    get_clients_db,
    get_client_by_naming,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from helper.array_helper import compare_lists_of_dictionaries

# Подготовленные для теста данные
data_for_client = make_data_all_client_fields()
edit_sign = "_ED"  # Метка для того, чтобы показать, какое значение было отредактировано


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsClientsAPI:
    @staticmethod
    @pytest.mark.order(1)
    @pytest.mark.regress()
    @allure.title(
        'Тест получает записи справочника Клиенты через API и сравнивает с данными из базы'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_clients_list_api(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        clients_from_db = get_clients_db()
        clients_from_server = get_clients_api(token)
        assert len(clients_from_db) == len(clients_from_server), "Длина, полученных списков неодинакова"

        # Подготовка данных, полученных с сервера. Там отличаются правила именования ключей.
        for each_record in clients_from_server:
            each_record['organization'] = each_record['organization']['id']
        for each_record in clients_from_server:
            each_record['acl_organization_id'] = each_record['organization']
            del each_record['organization']
        clients_from_server = humps.decamelize(clients_from_server)

        assert compare_lists_of_dictionaries(clients_from_db, clients_from_server), "Данные, полученные из" \
                                                                                    "базы, и данные, полу-" \
                                                                                    "-ченные от сервера, не" \
                                                                                    " совпадают"

    @staticmethod
    @pytest.mark.order(2)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет создания новой записи в справочнике Клиенты через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_client_api(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        created_result = create_client_admin_office(data_for_client['name'],
                                                    data_for_client['naming'],
                                                    data_for_client['fullName'],
                                                    data_for_client['inn'],
                                                    data_for_client['kpp'],
                                                    get_organization_id_by_name(data_for_client['organization']),
                                                    token)
        created_result['organization'] = created_result['organization']['id']
        get_client_data_from_db = get_client_by_naming(data_for_client['naming'])  # Получение данных из базы
        client_data_from_db_into_dict = {
            'id': str(get_client_data_from_db.id),
            'name': get_client_data_from_db.name,
            'naming': get_client_data_from_db.naming,
            'full_name': get_client_data_from_db.full_name,
            'inn': get_client_data_from_db.inn,
            'kpp': get_client_data_from_db.kpp,
            'organization': str(get_client_data_from_db.acl_organization_id),
        }
        assert humps.decamelize(created_result) == client_data_from_db_into_dict, 'Данные созданного клиента в БД и' \
                                                                                  'данные, полученные от сервера,' \
                                                                                  'не совпадают'

    @staticmethod
    @pytest.mark.order(3)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет редактирование новой записи в справочнике Клиенты через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_client_api(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        get_client_data_from_db = get_client_by_naming(data_for_client['naming'])
        client_data_from_db_into_dict = {
            'id': str(get_client_data_from_db.id),
            'name': get_client_data_from_db.name,
            'naming': get_client_data_from_db.naming,
            'full_name': get_client_data_from_db.full_name,
            'inn': get_client_data_from_db.inn,
            'kpp': get_client_data_from_db.kpp,
        }
        data_for_client['name'] = data_for_client['name'] + edit_sign
        data_for_client['fullName'] = data_for_client['fullName'] + edit_sign
        updated_result = update_client(client_data_from_db_into_dict['id'],
                                       data_for_client['name'],
                                       data_for_client['naming'],
                                       data_for_client['fullName'],
                                       data_for_client['inn'],
                                       data_for_client['kpp'],
                                       token)
        get_client_data_from_db = get_client_by_naming(data_for_client['naming'])
        client_data_from_db_into_dict['name'] = get_client_data_from_db.name
        client_data_from_db_into_dict['full_name'] = get_client_data_from_db.full_name
        assert humps.decamelize(updated_result) == client_data_from_db_into_dict, 'Данные отредактированного' \
                                                                                  ' клиента в БД и данные, ' \
                                                                                  'полученные от сервера, не совпадают'

    @staticmethod
    @pytest.mark.order(4)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет удаление созданной записи в справочнике Клиенты через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_client_api(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        get_client_data_from_db = get_client_by_naming(data_for_client['naming'])
        client_id_from_db_taken = str(get_client_data_from_db.id)
        result = delete_client_by_id(client_id_from_db_taken, token)
        assert result, "Кажется, запись не удалилась. Лучше перепроверить"
